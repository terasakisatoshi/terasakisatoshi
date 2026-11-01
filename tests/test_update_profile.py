import datetime
import importlib.util
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

spec = importlib.util.spec_from_file_location("update_profile", Path(__file__).resolve().parents[1] / "scripts/update_profile.py")
update_profile = importlib.util.module_from_spec(spec)
spec.loader.exec_module(update_profile)


class UpdateProfileTest(unittest.TestCase):
    def test_updates_card_numbers_and_accessible_description(self):
        svg = Path("assets/github-profile.svg").read_text()
        result = update_profile.update(svg, {"public_repos": 12, "public_gists": 34, "followers": 56}, datetime.date(2026, 12, 1))
        root = ET.fromstring(result)
        elements = {e.get("id"): e.text for e in root.iter() if e.get("id")}
        self.assertEqual([elements[k] for k in ("repos", "gists", "followers")], ["12", "34", "56"])
        self.assertIn("12 public repositories, 34 public gists, and 56 followers", elements["desc"])
        self.assertIn("December 2026", elements["snapshot"])

    def test_rejects_missing_or_invalid_values(self):
        svg = Path("assets/github-profile.svg").read_text()
        for profile in ({"public_repos": 1}, {"public_repos": -1, "public_gists": 2, "followers": 3}):
            with self.assertRaises((KeyError, ValueError)):
                update_profile.update(svg, profile, datetime.date(2026, 12, 1))


if __name__ == "__main__":
    unittest.main()
