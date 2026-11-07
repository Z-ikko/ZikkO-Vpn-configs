import asyncio
import base64
import binascii
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit
from uuid import UUID

LIMIT = 1500
CHUNK = 300
MAX_FILE = 8 * 1024 * 1024
TAGS = ["ZikkOVpnBot | نامحدود ماهی ۲۰۰ت", "ZikkOVpnBot | تست رایگان",
        "ZikkOVpnBot | کانفیگ مخصوص جمنای و انواع هوش مصنوعی"]
LINK = re.compile(r"""(?:vless|vmess|trojan|ss)://[^\s<>"`]+""", re.I)


def decode64(s):
    return base64.b64decode(s + "=" * (-len(s) % 4), altchars=b"-_", validate=True)


def rename(uri, tag):
    base = uri.partition("#")[0]
    scheme, data = base.split("://", 1)
    if scheme.lower() == "vmess":
        config = json.loads(decode64(data))
        if not isinstance(config, dict) or not config.get("add"):
            raise ValueError("vmess fields")
        UUID(config["id"])
        if not 1 <= int(config["port"]) <= 65535:
            raise ValueError("port")
        config["ps"] = tag
        encoded = json.dumps(config, ensure_ascii=False, separators=(",", ":")).encode()
        return "vmess://" + base64.b64encode(encoded).decode()
    if scheme.lower() == "ss" and "@" not in data:
        endpoint = urlsplit("ss://" + decode64(data).decode())
    else:
        endpoint = urlsplit(base)
    if not endpoint.hostname or not endpoint.port or not endpoint.username:
        raise ValueError("endpoint")
    if scheme.lower() == "vless":
        UUID(endpoint.username)
    return base + "#" + "".join(f"%{b:02X}" for b in tag.encode())


def extract(text):
    if not LINK.search(text):
        try:
            text = decode64("".join(text.split())).decode()
        except (ValueError, UnicodeError):
            return []
    result = []
    for uri in LINK.findall(text):
        try:
            result.append(rename(uri, ""))
        except (ValueError, KeyError, TypeError, AttributeError, binascii.Error, RecursionError):
            continue
    return result


def publish(folder, entries, cursors):
    if not entries:
        raise ValueError("empty snapshot")
    folder.mkdir(exist_ok=True)
    lines = [rename(uri, TAGS[i % 3]) for i, uri in enumerate(entries)]
    parts = [lines[i:i + CHUNK] for i in range(0, LIMIT, CHUNK)]
    if sum(parts, []) != lines:
        raise ValueError("snapshot mismatch")
    for name, rows in [("all", lines), *enumerate(parts, 1)]:
        (folder / f"{name}.txt").write_bytes("".join(row + "\n" for row in rows).encode())
    (folder / "cursor.json").write_text(json.dumps(cursors, sort_keys=True), encoding="utf8")


async def contents(client, msg, kind):
    if kind == "text":
        return msg.raw_text or ""
    file = msg.file
    if not file or not (file.name or "").lower().endswith(".txt"):
        return ""
    if not file.size or file.size > MAX_FILE:
        raise ValueError("unexpected file size")
    data = await asyncio.wait_for(client.download_media(msg, file=bytes), timeout=120)
    if not data or len(data) != file.size:
        raise ValueError("incomplete file")
    return data.decode("utf-16" if data.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8-sig")


async def collect(client, sources, previous, prior_entries):
    streams, heads, cursors = {}, {}, dict(previous)
    for source in sources:
        key = source["id"]
        peer = source["peer"]
        stream = aiter(client.iter_messages(peer, min_id=previous.get(key, 0)))
        streams[key] = stream
        head = await anext(stream, None)
        if head:
            heads[key] = head
            cursors[key] = head.id
    kinds = {s["id"]: s["kind"] for s in sources}
    fresh = []
    while heads and len(fresh) < LIMIT:
        key = max(heads, key=lambda k: (heads[k].date, k, heads[k].id))
        msg = heads[key]
        body = await contents(client, msg, kinds[key])
        rows = extract(body) if body else []
        if body and not rows and (kinds[key] == "txt" or LINK.search(body)):
            raise ValueError("config post unreadable: " + key)
        fresh.extend(rows[:LIMIT - len(fresh)])
        if len(fresh) < LIMIT:
            head = await anext(streams[key], None)
            if head is None:
                del heads[key]
            else:
                heads[key] = head
    return (fresh + prior_entries)[:LIMIT], cursors


async def main():
    from telethon import TelegramClient
    from telethon.sessions import StringSession
    sources = json.loads(Path("sources.json").read_text())
    folder = Path("sub")
    previous, entries = {}, []
    if folder.exists():
        previous = json.loads((folder / "cursor.json").read_text())
        entries = (folder / "all.txt").read_text(encoding="utf8").splitlines()
        if not entries:
            raise ValueError("invalid previous snapshot")
    client = TelegramClient(StringSession(os.environ["TG_SESSION"]), int(os.environ["TG_API_ID"]),
                            os.environ["TG_API_HASH"], request_retries=2, connection_retries=2)
    await client.connect()
    try:
        if not await client.is_user_authorized():
            raise RuntimeError("Telegram login required")
        sources[0]["peer"] = int(os.environ[sources[0]["peer_secret"]])
        async for dialog in client.iter_dialogs():
            if dialog.id == sources[0]["peer"]:
                sources[0]["peer"] = dialog.input_entity
                break
        else:
            raise ValueError("selected channel unavailable")
        for source in sources[1:]:
            source["peer"] = source["username"]
        rows, cursors = await collect(client, sources, previous, entries)
        publish(folder, rows, cursors)
        print(f"Subscription entries: {len(rows)}")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as error:
        print("Collection failed:", type(error).__name__, file=sys.stderr)
        sys.exit(1)
