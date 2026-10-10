#!/usr/bin/env python3
import json
import os
import re
import urllib.request

USERNAME = "lucasantannaeng"
README_PATH = os.path.join(os.path.dirname(__file__), "..", "README.md")
MAX_ACTIVITIES = 5

token = os.environ.get("GITHUB_TOKEN")
headers = {
    "User-Agent": "GitHub-Activity-Generator",
    "Accept": "application/vnd.github.v3+json",
}
if token:
    headers["Authorization"] = f"token {token}"


def fetch_json(url):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def get_activities():
    events_url = f"https://api.github.com/users/{USERNAME}/events?per_page=100"
    events = fetch_json(events_url)
    if not events:
        return []

    activities = []
    seen = set()

    for e in events:
        etype = e.get("type")
        repo_name = e.get("repo", {}).get("name", "")
        repo_url = f"https://github.com/{repo_name}"

        if etype == "PushEvent":
            head = e.get("payload", {}).get("head")
            if not head:
                continue
            key = (repo_name, head)
            if key in seen:
                continue
            seen.add(key)

            # Fetch commit message
            commit_data = fetch_json(f"https://api.github.com/repos/{repo_name}/commits/{head}")
            raw_msg = (
                commit_data.get("commit", {}).get("message", "Update repository")
                if commit_data
                else "Update repository"
            )
            clean_msg = raw_msg.split("\n")[0].strip()
            if len(clean_msg) > 60:
                clean_msg = clean_msg[:57] + "..."

            short_sha = head[:7]
            commit_url = f"{repo_url}/commit/{head}"
            activities.append(
                f"🔨 Pushed [`{short_sha}`]({commit_url}) to [{repo_name}]({repo_url}) - *{clean_msg}*"
            )

        elif etype == "PullRequestEvent":
            action = e.get("payload", {}).get("action", "")
            pr = e.get("payload", {}).get("pull_request", {})
            pr_num = pr.get("number")
            pr_title = pr.get("title", "")
            pr_url = pr.get("html_url", f"{repo_url}/pull/{pr_num}")
            key = (repo_name, pr_num, action)
            if key in seen:
                continue
            seen.add(key)

            icon = "🎉" if action == "closed" and pr.get("merged") else "💪"
            activities.append(
                f"{icon} {action.capitalize()} PR [#{pr_num}]({pr_url}) in [{repo_name}]({repo_url}) - *{pr_title}*"
            )

        elif etype == "ReleaseEvent":
            rel = e.get("payload", {}).get("release", {})
            tag = rel.get("tag_name", "")
            rel_url = rel.get("html_url", f"{repo_url}/releases/tag/{tag}")
            activities.append(f"🚀 Published release [{tag}]({rel_url}) in [{repo_name}]({repo_url})")

        if len(activities) >= MAX_ACTIVITIES:
            break

    return activities


def update_readme(activities):
    if not os.path.exists(README_PATH):
        print(f"README not found at {README_PATH}")
        return False

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"<!--START_SECTION:activity-->[\s\S]*?<!--END_SECTION:activity-->"
    if not re.search(pattern, content):
        print("Activity section markers not found in README.")
        return False

    formatted = "\n".join([f"{idx + 1}. {act}" for idx, act in enumerate(activities)])
    replacement = f"<!--START_SECTION:activity-->\n{formatted}\n<!--END_SECTION:activity-->"

    new_content = re.sub(pattern, replacement, content)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("README successfully updated with recent activities.")
    return True


if __name__ == "__main__":
    acts = get_activities()
    if acts:
        update_readme(acts)
    else:
        print("No activities found.")
