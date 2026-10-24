import unittest
from pathlib import Path

from update_cryptomator import PLATFORMS, RELEASE_ROOT, release_assets, update_formula


def release(version="0.6.2", platforms=PLATFORMS):
    return {
        "tag_name": version,
        "assets": [
            {
                "name": f"cryptomator-cli-{version}-{platform}.zip",
                "browser_download_url": (
                    f"{RELEASE_ROOT}/{version}/cryptomator-cli-{version}-{platform}.zip"
                ),
            }
            for platform in platforms
        ],
    }


class UpdateTests(unittest.TestCase):
    def test_missing_mac_arm_skips_release(self):
        version, urls, missing = release_assets(release(platforms=PLATFORMS[1:]))
        self.assertEqual(version, "0.6.2")
        self.assertEqual(urls, {})
        self.assertEqual(missing, ["cryptomator-cli-0.6.2-mac-arm64.zip"])

    def test_complete_release_updates_all_platforms(self):
        _, urls, missing = release_assets(release())
        self.assertEqual(missing, [])
        formula = Path(__file__).resolve().parents[2] / "Formula/cryptomator-cli.rb"
        original = formula.read_text()
        updated = update_formula(original, urls, lambda _: "a" * 64)
        for url in urls.values():
            self.assertIn(f'url "{url}"', updated)
        self.assertEqual(updated.count(f'sha256 "{"a" * 64}"'), 4)
        self.assertEqual(updated[updated.index("  def install"):],
                         original[original.index("  def install"):])

    def test_unexpected_asset_host_rejected(self):
        data = release()
        data["assets"][0]["browser_download_url"] = "https://example.com/file.zip"
        with self.assertRaises(ValueError):
            release_assets(data)

    def test_unsafe_tag_rejected(self):
        with self.assertRaises(ValueError):
            release_assets(release(version="0.6.2\nchanged=true"))

    def test_prerelease_rejected(self):
        data = release()
        data["prerelease"] = True
        with self.assertRaises(ValueError):
            release_assets(data)

    def test_incomplete_formula_rejected(self):
        _, urls, _ = release_assets(release())
        with self.assertRaises(ValueError):
            update_formula("", urls, lambda _: "a" * 64)

    def test_invalid_checksum_rejected(self):
        _, urls, _ = release_assets(release())
        formula = Path(__file__).resolve().parents[2] / "Formula/cryptomator-cli.rb"
        with self.assertRaises(ValueError):
            update_formula(formula.read_text(), urls, lambda _: "invalid")


if __name__ == "__main__":
    unittest.main()
