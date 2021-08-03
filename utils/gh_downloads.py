#!/usr/bin/env python3
"""
Retrieves the GH releases stats from their open API and counts the total number
of asset downloads, which so far are all Mu installers.
"""
import requests


releases = requests.get(
    "https://api.github.com/repos/mu-editor/mu/releases"
).json()

total_downloads = 0
for release in releases:
    date = release["published_at"].split("T")[0]
    print("\nRelease {} ({}):".format(release["tag_name"], date))

    if "assets" in release and len(release["assets"]):
        for asset in release["assets"]:
            total_downloads += asset["download_count"]
            print(
                "\tDownloads: {:6}".format(asset["download_count"]), end="\t"
            )
            print("Asset: {}".format(asset["name"]))
    else:
        print("\tNo assets on this release")

print("\nTotal Mu Editor asset downloads: {}  🎉".format(total_downloads))
