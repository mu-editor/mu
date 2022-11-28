#!/usr/bin/env python3
"""
Retrieves the GH releases stats from their open API and counts the total number
of asset downloads, which so far are all Mu installers.
"""
import datetime
import requests


releases = requests.get(
    "https://api.github.com/repos/mu-editor/mu/releases"
).json()

# First generate date objects for each release and add them to their dictionary
for release in releases:
    date_str = release["published_at"].split("T")[0]
    release["date_processed"] = datetime.date.fromisoformat(date_str)

total_downloads = 0

# Print the release info in reverse order, old to new
reversed_releases = releases[::-1]
for i, release in enumerate(reversed_releases):
    if i < (len(reversed_releases) - 1):
        next_date = reversed_releases[i + 1]["date_processed"]
    else:
        next_date = datetime.date.today()
    diff_date = next_date - release["date_processed"]
    months_days_diff = divmod(diff_date.days, 30)
    print(
        "\nRelease {} ({}, {} months and {} days):".format(
            release["tag_name"],
            release["date_processed"],
            months_days_diff[0],
            months_days_diff[1],
        )
    )

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
