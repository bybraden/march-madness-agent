# 🏀 March Madness Agent

A simple Python-based AI agent that predicts NCAA March Madness game winners using **real 2025-26 season team statistics**.

## Project Structure

```
march-madness-agent/
├── data/
│   └── teams.csv          # Real 2025-26 season stats for 50 tournament teams
├── outputs/
│   └── predictions.txt    # Saved prediction results (auto-generated)
├── src/
│   ├── predictor.py       # Core prediction logic (MarchMadnessAgent class)
│   └── main.py            # CLI entry point
├── requirements.txt
└── README.md
```

## Data Source

Stats from **Sports-Reference.com** — 2025-26 Men's College Basketball season.

- **Season:** 2025-26 (regular season + conference tournaments)
- **Teams included:** 50 NCAA tournament teams (2026 field)
- **Columns:** `team`, `seed`, `wins`, `losses`, `ppg` (points per game), `oppg` (opponent points per game)

### 2026 Tournament #1 Seeds
| Seed | Team | Record |
|------|------|--------|
| 1 | Duke | 32-2 |
| 1 | Arizona | 32-2 |
| 1 | Michigan | 31-3 |
| 1 | Florida | 26-7 |

## How It Works

The agent uses a composite scoring formula:

| Factor | Weight |
|--------|--------|
| Seed (lower = better) | `(16 - seed) × 3` |
| Win count | `wins × 1.0` |
| Points per game (offense) | `ppg × 0.5` |
| Opponent PPG (defense) | `(100 - oppg) × 0.5` |

The team with the higher composite score is predicted to win along with a confidence margin.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/bybraden/march-madness-agent.git
cd march-madness-agent
```

### 2. (Optional) Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Run

```bash
python src/main.py
```

## Example Usage

```
=======================================================
       🏀  March Madness Prediction Agent  🏀
=======================================================

Loaded 50 teams from data/teams.csv

Enter Team 1: Duke
Enter Team 2: Houston

-------------------------------------------------------
  🏆  Predicted Winner: Duke
-------------------------------------------------------
  Duke (#1 seed) is predicted to beat Houston (#2 seed).

  Duke stats:  32-2 record, 81.9 PPG, 63.1 OPPG  [Score: 131.4]
  Houston stats:  28-6 record, 77.5 PPG, 62.2 OPPG  [Score: 119.65]

  Confidence margin: 11.75 points
  Moderate edge for the predicted winner.

Result saved to: outputs/predictions.txt
=======================================================
```

## Available Teams (2026 NCAA Tournament Field)

| Team | Seed | Record | PPG | OPPG |
|------|------|--------|-----|------|
| Duke | 1 | 32-2 | 81.9 | 63.1 |
| Arizona | 1 | 32-2 | 86.1 | 68.4 |
| Michigan | 1 | 31-3 | 87.4 | 69.6 |
| Florida | 1 | 26-7 | 87.1 | 71.5 |
| UConn | 2 | 29-5 | 77.6 | 65.3 |
| Purdue | 2 | 29-8 | 82.2 | 70.1 |
| Iowa State | 2 | 29-7 | 82.5 | 65.3 |
| Houston | 2 | 28-6 | 77.5 | 62.2 |
| Michigan State | 3 | 27-7 | 79.3 | 68.4 |
| Gonzaga | 3 | 31-4 | 84.3 | 66.2 |
| Illinois | 3 | 26-8 | 84.7 | 69.4 |
| Virginia | 3 | 30-6 | 80.4 | 68.8 |
| St. John's | 5 | 30-6 | 81.1 | 69.4 |
| Kansas | 6 | 24-11 | 75.1 | 69.1 |
| Alabama | 6 | 25-9 | 91.6 | 82.5 |
| Arkansas | 8 | 28-8 | 90.2 | 80.2 |
| ... and 34 more | | | | |

Run the agent and type any team name to see the full list.

> **Note:** Stats are from the 2025-26 regular season and conference tournaments, sourced from Sports-Reference.com. Michigan (note: men's team) is a #1 seed in this cycle.
