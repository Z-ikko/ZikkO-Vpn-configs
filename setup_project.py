"""Local Windows setup. Secrets travel to gh only through stdin."""
import asyncio
import getpass
import subprocess
import sys
from pathlib import Path

from telethon import TelegramClient
from telethon.sessions import StringSession

NAME = "ZikkO-Vpn-configs"
FILES = ["collector.py", "setup_project.py", "setup.cmd", "sources.json",
         "wheels", "requirements.txt", "test_collector.py", "README.md", ".gitignore", ".github/workflows/update.yml"]


def run(*args, capture=False, secret=None):
    return subprocess.run(args, input=secret, text=True, encoding="utf8", check=True,
                          stdout=subprocess.PIPE if capture else None).stdout


async def telegram():
    api_id = input("Telegram API ID (my.telegram.org/apps): ").strip()
    api_hash = getpass.getpass("Telegram API hash (hidden): ").strip()
    while True:
        port_text = input("Local SOCKS5 port (press Enter for direct / TUN): ").strip()
        if port_text and (not port_text.isdecimal() or not 1 <= int(port_text) <= 65535):
            print("Enter a port number from 1 to 65535.")
            continue
        proxy = ("socks5", "127.0.0.1", int(port_text)) if port_text else None
        client = TelegramClient(StringSession(), int(api_id), api_hash, proxy=proxy,
                                connection_retries=1, timeout=10)
        try:
            await asyncio.wait_for(client.connect(), timeout=35)
            break
        except (OSError, asyncio.TimeoutError):
            await client.disconnect()
            print("Cannot reach Telegram. Check your VPN / local SOCKS5 port, then retry.")
    await client.start()
    try:
        chats = [dialog async for dialog in client.iter_dialogs()
                 if dialog.is_channel or dialog.is_group]
        for index, dialog in enumerate(chats, 1):
            print(index, dialog.name)
        choice = int(input("Number of YOUR source channel for public configs: "))
        if not 1 <= choice <= len(chats):
            raise ValueError("invalid channel selection")
        selected = chats[choice - 1]
        if not await client.get_messages(selected.input_entity, limit=1):
            raise ValueError("No readable posts in selected channel")
        if not await client.get_messages("proxy_kafee", limit=1):
            raise ValueError("No readable posts in proxy_kafee")
        return {"TG_API_ID": api_id, "TG_API_HASH": api_hash,
                "TG_SESSION": client.session.save(), "TG_OWN_PEER": str(selected.id)}
    finally:
        await client.disconnect()


def main():
    run("git", "--version")
    run("gh", "--version")
    if subprocess.run(["gh", "auth", "status"], capture_output=True).returncode:
        run("gh", "auth", "login", "--hostname", "github.com", "--web", "--git-protocol", "https", "--scopes", "workflow")
    owner = run("gh", "api", "user", "--jq", ".login", capture=True).strip()
    repo = f"{owner}/{NAME}"
    if input(f"Create or resume public project {repo}? Type its owner: ").strip() != owner:
        return
    url = f"https://github.com/{repo}.git"
    run("gh", "auth", "setup-git")
    if not Path(".git").exists():
        run("git", "init", "-b", "main")
    remotes = run("git", "remote", capture=True).splitlines()
    if "origin" in remotes and run("git", "remote", "get-url", "origin", capture=True).strip() != url:
        raise ValueError("Unexpected origin")
    if "origin" in remotes:
        run("git", "fetch", "origin")
        has_main = subprocess.run(["git", "show-ref", "--verify", "--quiet", "refs/remotes/origin/main"])
        if has_main.returncode == 0:
            run("git", "merge", "--ff-only", "origin/main")
    run("git", "add", "--", *FILES)
    if subprocess.run(["git", "diff", "--cached", "--quiet"]).returncode == 1:
        run("git", "-c", "user.name=ZikkO Vpn configs", "-c", "user.email=setup@users.noreply.github.com",
            "commit", "-m", "Set up ZikkO Vpn configs collector")
    if subprocess.run(["gh", "repo", "view", repo], capture_output=True).returncode:
        run("gh", "repo", "create", repo, "--public")
    visibility = run("gh", "repo", "view", repo, "--json", "visibility", "--jq", ".visibility", capture=True)
    if visibility.strip() != "PUBLIC":
        raise ValueError("Expected a public repository")
    if "origin" not in remotes:
        run("git", "remote", "add", "origin", url)
    run("git", "push", "-u", "origin", "main")
    run("gh", "repo", "edit", repo, "--description", "ZikkO Vpn configs",
        "--add-topic", "vpn", "--add-topic", "configs")
    secrets = asyncio.run(telegram())
    for key, value in secrets.items():
        run("gh", "secret", "set", key, "-R", repo, secret=value)
    run("gh", "workflow", "run", "update.yml", "-R", repo, "--ref", "main")
    print("Run status: https://github.com/" + repo + "/actions")
    print("After first successful publish:")
    for label in ["all", "1", "2", "3", "4", "5"]:
        print(f"https://raw.githubusercontent.com/{repo}/main/sub/{label}.txt")


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        sys.exit(str(error))
    except Exception as error:
        sys.exit("Setup stopped: " + type(error).__name__ + ". Check the preceding step and retry.")
