#!/usr/bin/env python3

import json
import re
import urllib.request

def get_org_repositories(org_name):
    url = f"https://api.github.com/orgs/{org_name}/repos"
    headers = {
        "Accept": "application/vnd.github+json",
    }
    request = urllib.request.Request(url, headers=headers)
    repositories = []
    while url:
        with urllib.request.urlopen(request) as response:
            if response.status != 200:
                raise Exception(f"Failed to fetch repositories: {response.status}")
            data = json.loads(response.read().decode())
            repositories.extend(repo["name"] for repo in data)
            # Check for the 'next' link in the response headers for pagination
            links = response.headers.get("Link", "")
            next_url = None
            for link in links.split(","):
                if 'rel="next"' in link:
                    next_url = link.split(";")[0].strip("<> ")
                    break
            url = next_url
            if url:
                request = urllib.request.Request(url, headers=headers)
    return sorted(repositories)

if __name__ == "__main__":
    lines = []
    table_begin_index = -1
    table_end_index = -1
    template = ""

    with open("security-dashboard.md", "r") as f:
        lines = [""] + f.readlines() + [""]

        for i, line in enumerate(lines):
            if re.match(r"^\|.*\|", line):
                if table_begin_index == -1:
                    table_begin_index = i
                if re.match(r"[^0-9A-Za-z\-]+sig-security[^0-9A-Za-z\-]+", line):
                    template = line
            else:
                if table_begin_index != -1:
                    if table_end_index == -1:
                        table_end_index = i - 1

    if template:
        output = lines[0 : table_begin_index + 2] + [
            template.replace("sig-security", repo)
            for repo in get_org_repositories("open-telemetry")
        ] + lines[table_end_index + 1:]
        print("".join(output))
