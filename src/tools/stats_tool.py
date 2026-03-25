import re
import unicodedata
import warnings
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup, Comment


SEASON_YEAR = 2026
SPORTS_REFERENCE_BASE = "https://www.sports-reference.com"
SCHOOL_STATS_URL = f"{SPORTS_REFERENCE_BASE}/cbb/seasons/men/{SEASON_YEAR}-school-stats.html"

EXPLICIT_SLUG_MAP = {
    "UConn": "connecticut",
    "St. John's": "st-johns-ny",
}

EXPLICIT_TABLE_NAME_MAP = {
    "UConn": ["Connecticut", "UConn"],
    "St. John's": ["St. John's (NY)", "St. John's"],
}

warnings.filterwarnings("ignore")


def normalize_text_for_slug(name: str) -> str:
    text = unicodedata.normalize("NFKD", name)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower().strip()
    text = text.replace(".", "")
    text = text.replace("'", "")
    text = text.replace("&", "and")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text


def resolve_school_slug(bracket_team_name: str) -> str:
    if bracket_team_name in EXPLICIT_SLUG_MAP:
        return EXPLICIT_SLUG_MAP[bracket_team_name]
    return normalize_text_for_slug(bracket_team_name)


def get_table_name_candidates(bracket_team_name: str) -> List[str]:
    if bracket_team_name in EXPLICIT_TABLE_NAME_MAP:
        return EXPLICIT_TABLE_NAME_MAP[bracket_team_name]
    return [bracket_team_name]


def build_team_season_url(bracket_team_name: str, season_year: int = SEASON_YEAR) -> str:
    slug = resolve_school_slug(bracket_team_name)
    return f"{SPORTS_REFERENCE_BASE}/cbb/schools/{slug}/men/{season_year}.html"


def request_text(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers, timeout=20)
    if response.status_code != 200:
        raise ValueError(f"Request failed for {url} (status code {response.status_code})")

    return response.text


def build_all_soups(html: str) -> List[BeautifulSoup]:
    soups: List[BeautifulSoup] = []

    main_soup = BeautifulSoup(html, "html.parser")
    soups.append(main_soup)

    for comment in main_soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment_text = str(comment)
        if "<table" in comment_text or "<div" in comment_text:
            soups.append(BeautifulSoup(comment_text, "html.parser"))

    return soups


def extract_school_stats_row(bracket_team_name: str) -> Optional[Dict[str, str]]:
    html = request_text(SCHOOL_STATS_URL)
    soups = build_all_soups(html)
    candidates = get_table_name_candidates(bracket_team_name)

    for soup in soups:
        for table in soup.find_all("table"):
            tbody = table.find("tbody")
            if not tbody:
                continue

            for row in tbody.find_all("tr"):
                classes = row.get("class", [])
                if "thead" in classes:
                    continue

                header = row.find("th")
                if not header:
                    continue

                row_name = header.get_text(" ", strip=True)

                if row_name not in candidates:
                    continue

                data = {
                    "_matched_name": row_name,
                    "_table_id": table.get("id", ""),
                }

                header_stat = header.get("data-stat")
                if header_stat:
                    data[header_stat] = row_name

                for cell in row.find_all(["td", "th"]):
                    data_stat = cell.get("data-stat")
                    if not data_stat:
                        continue
                    data[data_stat] = cell.get_text(" ", strip=True)

                return data

    return None


if __name__ == "__main__":
    test_team = "Duke"

    row = extract_school_stats_row(test_team)

    if row is None:
        print("NO ROW FOUND")
    else:
        print("ROW FOUND")
        print("Matched name:", row.get("_matched_name"))
        print("Table id:", row.get("_table_id"))
        print()

        for key in sorted(row.keys()):
            print(f"{key}: {row[key]}")

