import asyncio
import base64
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import unquote
from unittest.mock import AsyncMock

from collector import collect, extract, publish, rename, TAGS

URI = "vless://00000000-0000-4000-8000-000000000001@example.org:443?path=%2Fa&type=ws"
SOURCES = [{"id": "a", "peer": "a", "kind": "text"}, {"id": "b", "peer": "b", "kind": "txt"}]


class Client:
    def __init__(self, messages):
        self.messages = messages

    async def iter_messages(self, peer, min_id):
        for msg in self.messages[peer]:
            if msg.id > min_id:
                yield msg


class Tests(unittest.TestCase):
    def test_formats(self):
        raw = {"id": "00000000-0000-4000-8000-000000000001", "add": "example.org", "port": "443"}
        vm = "vmess://" + base64.b64encode(json.dumps(raw).encode()).decode()
        body = "\n".join([URI, vm, "trojan://sample@example.org:443", "ss://YWVzOnB3@example.org:443"])
        rows = extract(base64.b64encode(body.encode()).decode())
        self.assertEqual(len(rows), 4)
        self.assertEqual(extract("vmess://broken"), [])
        self.assertEqual(json.loads(base64.b64decode(rename(rows[1], TAGS[1])[8:])), dict(raw, ps=TAGS[1]))

    def test_bootstrap_refresh_retry(self):
        text = SimpleNamespace(id=12, date=2, raw_text=URI)
        file = SimpleNamespace(id=27, date=3, file=SimpleNamespace(name="240ta.txt", size=len(URI)))
        client = Client({"a": [text], "b": [file]})
        client.download_media = AsyncMock(return_value=URI.encode())
        rows, state = asyncio.run(collect(client, SOURCES, {}, []))
        self.assertEqual(len(rows), 2)
        self.assertEqual(state, {"a": 12, "b": 27})
        self.assertEqual(asyncio.run(collect(client, SOURCES, state, rows)), (rows, state))
        text.id += 1
        text.raw_text = "\n".join([URI] * 72)
        old = [URI + "&n=" + str(i) for i in range(1500)]
        updated, _ = asyncio.run(collect(client, SOURCES, state, old))
        self.assertEqual(updated[72:], old[:-72])
        client.download_media = AsyncMock(return_value=b"")
        with self.assertRaises(ValueError):
            asyncio.run(collect(client, SOURCES, {}, []))

    def test_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            publish(folder, [URI] * 1500, {"a": 23})
            rows = (folder / "all.txt").read_bytes().splitlines()
            parts = [(folder / f"{i}.txt").read_bytes().splitlines() for i in range(1, 6)]
            self.assertEqual([len(p) for p in parts], [300] * 5)
            self.assertEqual(sum(parts, []), rows)
            for i, row in enumerate(rows):
                prefix, tag = row.decode("ascii").split("#")
                self.assertEqual(prefix, URI)
                self.assertTrue(tag.startswith("%5A"))
                self.assertEqual(unquote(tag), TAGS[i % 3])
            with self.assertRaises(ValueError):
                publish(folder, [], {})
            self.assertEqual((folder / "all.txt").read_bytes().splitlines(), rows)
