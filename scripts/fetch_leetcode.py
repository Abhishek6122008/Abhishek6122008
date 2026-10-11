"""Public LeetCode stats from the GraphQL API (no login needed) -> data/leetcode.json
LeetCode sometimes blocks CI runners; on failure the previous data/leetcode.json is kept."""
import json
from datetime import datetime, timedelta, timezone

import requests

from common import load, save
from config import LEETCODE_USER

API = "https://leetcode.com/graphql"
QUERY = """
query profile($u: String!) {
  allQuestionsCount { difficulty count }
  matchedUser(username: $u) {
    profile { ranking }
    submitStatsGlobal { acSubmissionNum { difficulty count } }
    problemsSolvedBeatsStats { difficulty percentage }
    userCalendar { streak totalActiveDays submissionCalendar }
    badges { displayName }
    languageProblemCount { languageName problemsSolved }
    tagProblemCounts {
      advanced { tagName problemsSolved }
      intermediate { tagName problemsSolved }
      fundamental { tagName problemsSolved }
    }
  }
  userContestRanking(username: $u) { attendedContestsCount rating globalRanking topPercentage badge { name } }
}"""


def main():
    try:
        resp = requests.post(
            API,
            json={"query": QUERY, "variables": {"u": LEETCODE_USER}},
            headers={"Referer": f"https://leetcode.com/u/{LEETCODE_USER}/", "User-Agent": "Mozilla/5.0 profile-art"},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()["data"]
        user = data["matchedUser"]
        if not user:
            raise ValueError(f"LeetCode user {LEETCODE_USER!r} not found")
    except (requests.RequestException, ValueError, KeyError, TypeError) as e:
        if load("leetcode.json"):
            print(f"LeetCode fetch failed ({e}); keeping previous data/leetcode.json")
            return
        raise SystemExit(f"LeetCode fetch failed and no previous data: {e}")

    cal = {
        datetime.fromtimestamp(int(ts), timezone.utc).date().isoformat(): n
        for ts, n in json.loads(user["userCalendar"]["submissionCalendar"] or "{}").items()
    }
    # Current streak: today may still be empty, so start from yesterday in that case.
    day = datetime.now(timezone.utc).date()
    if day.isoformat() not in cal:
        day -= timedelta(days=1)
    current = 0
    while day.isoformat() in cal:
        current += 1
        day -= timedelta(days=1)

    tags = {}
    for level in user["tagProblemCounts"].values():
        for t in level:
            tags[t["tagName"]] = t["problemsSolved"]
    contest = data.get("userContestRanking")

    save("leetcode.json", {
        "username": LEETCODE_USER,
        "solved": {s["difficulty"]: s["count"] for s in user["submitStatsGlobal"]["acSubmissionNum"]},
        "total": {q["difficulty"]: q["count"] for q in data["allQuestionsCount"]},
        "beats": {b["difficulty"]: b["percentage"] for b in user.get("problemsSolvedBeatsStats") or [] if b["percentage"] is not None},
        "ranking": user["profile"]["ranking"],
        "contest": contest and {
            "rating": contest["rating"],
            "attended": contest["attendedContestsCount"],
            "global_ranking": contest["globalRanking"],
            "top_percentage": contest["topPercentage"],
            "badge": (contest.get("badge") or {}).get("name"),
        },
        "current_streak": current,
        "max_streak": user["userCalendar"]["streak"],
        "active_days": user["userCalendar"]["totalActiveDays"],
        "badges": [b["displayName"] for b in user["badges"]],
        "languages": {l["languageName"]: l["problemsSolved"] for l in sorted(user["languageProblemCount"], key=lambda l: -l["problemsSolved"])},
        "top_tags": dict(sorted(tags.items(), key=lambda t: -t[1])[:8]),
        "calendar": dict(sorted(cal.items())),
    })
    print(f"LeetCode: {user['submitStatsGlobal']['acSubmissionNum'][0]['count']} solved, streak {current}")


if __name__ == "__main__":
    main()
