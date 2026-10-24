"""Propose complete ARM64 updates without dropping required release assets."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.request


PLATFORMS = ("mac-arm64", "linux-aarch64")
RELEASE_ROOT = "https://github.com/cryptomator/cli/releases/download"
ARCHIVE = re.compile(
    r'(?P<prefix>url ")'
    + re.escape(RELEASE_ROOT)
    + r'/[^"\n]+/cryptomator-cli-[^"\n]+-'
    + r'(?P<platform>mac-arm64|linux-aarch64)\.zip'
    + r'(?P<middle>"\s+sha256 ")[0-9a-f]{64}"'
)


def release_assets(release):
    version = release["tag_name"]
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError(f"Unsupported release tag: {version!r}")
    if release.get("draft") or release.get("prerelease"):
        raise ValueError("Expected a stable, published release")
    assets = {asset["name"]: asset for asset in release["assets"]}
    names = {
        platform: f"cryptomator-cli-{version}-{platform}.zip"
        for platform in PLATFORMS
    }
    missing = [name for name in names.values() if name not in assets]
    if missing:
        return version, {}, missing
    urls = {}
    for platform, name in names.items():
        url = assets[name]["browser_download_url"]
        if url != f"{RELEASE_ROOT}/{version}/{name}":
            raise ValueError(f"Unexpected release asset URL: {url}")
        urls[platform] = url
    return version, urls, []


def update_formula(text, urls, checksum):
    platforms = [match["platform"] for match in ARCHIVE.finditer(text)]
    if sorted(platforms) != sorted(PLATFORMS):
        raise ValueError("Formula must contain exactly one archive per platform")

    def replace(match):
        url = urls[match["platform"]]
        digest = checksum(url)
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError("Invalid SHA256 checksum")
        return f'{match["prefix"]}{url}{match["middle"]}{digest}"'

    return ARCHIVE.sub(replace, text)


def checksum(url):
    digest = hashlib.sha256()
    with urllib.request.urlopen(url, timeout=120) as response:
        while chunk := response.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def report(message):
    print(message)
    if summary := os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(summary, "a") as output:
            output.write(message + "\n")


def main():
    release = json.loads(subprocess.check_output(
        ["gh", "api", "repos/cryptomator/cli/releases/latest"], text=True
    ))
    version, urls, missing = release_assets(release)
    if missing:
        report(f"Skipped {version}: missing required assets: {', '.join(missing)}")
        return
    path = Path(__file__).resolve().parents[2] / "Formula/cryptomator-cli.rb"
    original = path.read_text()
    if all(f'url "{url}"' in original for url in urls.values()):
        report(f"Formula already uses {version}.")
        return
    updated = update_formula(original, urls, checksum)
    path.write_text(updated)
    report(f"Prepared {version}: both ARM64 platform archives downloaded and hashed.")
    if output_path := os.environ.get("GITHUB_OUTPUT"):
        with open(output_path, "a") as output:
            output.write(f"changed=true\nversion={version}\n")


if __name__ == "__main__":
    main()
