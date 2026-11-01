"""Update the checked-in profile card from GitHub's user API response on stdin."""

import datetime
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

CARD = Path(__file__).resolve().parents[1] / "assets/github-profile.svg"
ET.register_namespace("", "http://www.w3.org/2000/svg")


def update(svg, profile, date):
    repos, gists, followers = (profile[key] for key in ("public_repos", "public_gists", "followers"))
    if any(type(value) is not int or value < 0 for value in (repos, gists, followers)):
        raise ValueError("Profile counts must be non-negative integers")
    month = date.strftime("%B %Y")
    root = ET.fromstring(svg)
    elements = {element.get("id"): element for element in root.iter() if element.get("id")}
    for key, value in (("repos", repos), ("gists", gists), ("followers", followers)):
        elements[key].text = str(value)
    elements["desc"].text = (f"{repos} public repositories, {gists} public gists, and {followers} followers. "
                             f"Snapshot from {month}. Interests include Julia, Python, and mathematics.")
    elements["snapshot"].text = f"GitHub public profile snapshot · {month}"
    return ET.tostring(root, encoding="unicode") + "\n"


if __name__ == "__main__":
    result = update(CARD.read_text(), json.load(sys.stdin), datetime.datetime.now(datetime.timezone.utc).date())
    CARD.write_text(result)
