# 🏀 March Madness Agent

A simple Python-based AI agent that predicts NCAA March Madness game winners using team statistics.

## Project Structure

```
march-madness-agent/
├── data/
│   └── teams.csv          # Team statistics dataset
├── outputs/
│   └── predictions.txt    # Saved prediction results (auto-generated)
├── src/
│   ├── predictor.py       # Core prediction logic (MarchMadnessAgent class)
│   └── main.py            # CLI entry point
├── requirements.txt
└── README.md
```

## How It Works

The agent reads team stats from `data/teams.csv` and uses a simple scoring formula:

| Factor | Weight |
|--------|--------|
| Seed (lower = better) | `(16 - seed) × 3` |
| Win count | `wins × 1.0` |
| Points per game (PPG) | `ppg × 0.5` |
| Opponent PPG (defense) | `(100 - oppg) × 0.5` |

The team with the higher composite score is predicted to win.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/bradenkindred/march-madness-agent.git
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

Available teams:
  - Duke
  - Houston
  - Kansas
  - UConn
  - Purdue
  - North Carolina
  - Tennessee
  - Alabama
  - Gonzaga
  - Marquette

Enter Team 1: UConn
Enter Team 2: Duke

-------------------------------------------------------
  🏆  Predicted Winner: UConn
-------------------------------------------------------
  UConn (#1 seed) is predicted to beat Duke (#2 seed).

  UConn stats:  31-3 record, 81.4 PPG, 63.2 OPPG  [Score: 123.6]
  Duke stats:   27-8 record, 80.1 PPG, 68.4 OPPG  [Score: 110.35]

  Confidence margin: 13.25 points
  Moderate edge for the predicted winner.

Result saved to: outputs/predictions.txt
=======================================================
```

Prediction results are appended to `outputs/predictions.txt` with a timestamp after each run.

## Available Teams

| Team | Seed | Record | PPG | OPPG |
|------|------|--------|-----|------|
| Duke | 2 | 27-8 | 80.1 | 68.4 |
| Houston | 1 | 30-4 | 74.3 | 57.9 |
| Kansas | 4 | 23-10 | 75.2 | 68.8 |
| UConn | 1 | 31-3 | 81.4 | 63.2 |
| Purdue | 1 | 29-4 | 83.9 | 70.1 |
| North Carolina | 1 | 27-7 | 81.7 | 70.3 |
| Tennessee | 2 | 24-8 | 79.1 | 67.2 |
| Alabama | 4 | 21-11 | 90.8 | 81.1 |
| Gonzaga | 5 | 25-7 | 84.6 | 70.3 |
| Marquette | 2 | 25-9 | 78.6 | 69.4 |
