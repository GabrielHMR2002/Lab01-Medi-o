import csv
import json
import os

def save_csv(repos, filename):
    if not repos:
        return
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    fieldnames = [
        "nameWithOwner", "url", "createdAt", "pushedAt", "description",
        "stargazerCount", "forkCount", "watchersCount",
        "issuesOpen", "issuesClosed",
        "pullRequestsOpen", "pullRequestsMerged", "pullRequestsClosed",
        "releasesCount", "primaryLanguage", "diskUsage",
        "licenseName", "licenseSpdx", "topics"
    ]
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for r in repos:
            writer.writerow({
                "nameWithOwner": r.get("nameWithOwner", ""),
                "url": r.get("url", ""),
                "createdAt": r.get("createdAt", ""),
                "pushedAt": r.get("pushedAt", ""),
                "description": r.get("description", ""),
                "stargazerCount": r.get("stargazerCount", 0),
                "forkCount": r.get("forkCount", 0),
                "watchersCount": (r.get("watchers") or {}).get("totalCount", 0),
                "issuesOpen": (r.get("issues") or {}).get("totalCount", 0),
                "issuesClosed": (r.get("issuesClosed") or {}).get("totalCount", 0),
                "pullRequestsOpen": (r.get("pullRequests") or {}).get("totalCount", 0),
                "pullRequestsMerged": (r.get("pullRequestsMerged") or {}).get("totalCount", 0),
                "pullRequestsClosed": (r.get("pullRequestsClosed") or {}).get("totalCount", 0),
                "releasesCount": (r.get("releases") or {}).get("totalCount", 0),
                "primaryLanguage": (r.get("primaryLanguage") or {}).get("name", ""),
                "diskUsage": r.get("diskUsage", 0),
                "licenseName": (r.get("licenseInfo") or {}).get("name", ""),
                "licenseSpdx": (r.get("licenseInfo") or {}).get("spdxId", ""),
                "topics": ",".join([t["topic"]["name"] for t in (r.get("topics") or {}).get("nodes", [])])
            })

def save_json(repos, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(repos, f, ensure_ascii=False, indent=4)
