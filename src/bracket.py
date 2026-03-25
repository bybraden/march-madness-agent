import re
from dataclasses import dataclass
from typing import List, Optional

import requests
from bs4 import BeautifulSoup


NCAA_BRACKET_URL = (
    "https://www.ncaa.com/news/basketball-men/mml-official-bracket/"
    "2026-03-23/2026-ncaa-tournament-bracket-schedule-scores-march-madness"
)


@dataclass
class Matchup:
    team1: str
    team2: str
    seed1: Optional[int] = None
    seed2: Optional[int] = None


def fetch_bracket_page_text() -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(NCAA_BRACKET_URL, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text("\n", strip=True)


def extract_sweet_16_matchups(page_text: str) -> List[Matchup]:
    lines = [line.strip() for line in page_text.splitlines() if line.strip()]

    start_idx = None
    end_idx = None

    for i, line in enumerate(lines):
        if "Thursday, March 26 (Sweet 16)" in line:
            start_idx = i
            break

    if start_idx is None:
        raise ValueError("Could not find Sweet 16 section on NCAA bracket page.")

    for i in range(start_idx + 1, len(lines)):
        if "Elite Eight" in lines[i]:
            end_idx = i
            break

    if end_idx is None:
        end_idx = len(lines)

    sweet_16_lines = lines[start_idx:end_idx]

    pattern = re.compile(
        r"^\((\d+)\)\s+(.+?)\s+vs\.\s+\((\d+)\)\s+(.+?)(?:,\s+\d{1,2}:\d{2}\s*p\.m\..*)?$"
    )

    matchups: List[Matchup] = []

    for line in sweet_16_lines:
        match = pattern.match(line)
        if not match:
            continue

        seed1 = int(match.group(1))
        team1 = match.group(2).strip()
        seed2 = int(match.group(3))
        team2 = match.group(4).strip()

        matchups.append(
            Matchup(
                team1=team1,
                team2=team2,
                seed1=seed1,
                seed2=seed2,
            )
        )

    if not matchups:
        raise ValueError("Found Sweet 16 section, but no matchup lines were parsed.")

    return matchups


def get_current_matchups() -> List[Matchup]:
    page_text = fetch_bracket_page_text()
    return extract_sweet_16_matchups(page_text)


if __name__ == "__main__":
    matchups = get_current_matchups()

    for i, matchup in enumerate(matchups, start=1):
        print(f"{i}. ({matchup.seed1}) {matchup.team1} vs ({matchup.seed2}) {matchup.team2}")


