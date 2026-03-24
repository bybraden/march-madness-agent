"""
March Madness Predictor
A simple AI agent that predicts NCAA tournament game winners based on team stats.
"""

import pandas as pd
import os


class MarchMadnessAgent:
    """A simple agent that predicts March Madness game outcomes using team statistics."""

    def __init__(self, csv_path: str):
        """
        Initialize the agent by loading team data from a CSV file.

        Args:
            csv_path: Path to the teams CSV file.
        """
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Data file not found: {csv_path}")

        self.data = pd.read_csv(csv_path)
        self.data["team"] = self.data["team"].str.strip()
        print(f"Loaded {len(self.data)} teams from {csv_path}")

    def get_team_stats(self, team_name: str) -> dict:
        """
        Retrieve stats for a given team.

        Supports case-insensitive exact matching first, then falls back to
        partial/fuzzy matching (ignoring punctuation) for convenience.

        Args:
            team_name: The name of the team (e.g. "Duke", "st johns", "Michigan St").

        Returns:
            A dictionary of team statistics.

        Raises:
            ValueError: If the team is not found in the dataset.
        """
        query = team_name.strip().lower()

        # 1. Exact case-insensitive match
        match = self.data[self.data["team"].str.lower() == query]

        # 2. Partial match — strip punctuation and check if query is a substring
        if match.empty:
            import re
            def normalize(s):
                return re.sub(r"[^a-z0-9 ]", "", s.lower())

            norm_query = normalize(query)
            mask = self.data["team"].apply(lambda t: norm_query in normalize(t))
            match = self.data[mask]

        if match.empty:
            available = "\n  ".join(sorted(self.data["team"].tolist()))
            raise ValueError(
                f"Team '{team_name}' not found in dataset.\n\nAvailable teams:\n  {available}"
            )

        if len(match) > 1:
            # Prefer the shortest name (most specific match)
            match = match.loc[[match["team"].str.len().idxmin()]]

        return match.iloc[0].to_dict()

    def _compute_score(self, stats: dict) -> float:
        """
        Compute a composite score for a team based on their statistics.

        Scoring formula:
        - Lower seed is better (inverted and weighted)
        - More wins = better
        - Higher points per game = better
        - Lower opponent points per game = better (defensive strength)

        Args:
            stats: Dictionary of team statistics.

        Returns:
            A float score (higher = stronger team).
        """
        seed_score = (16 - stats["seed"]) * 3      # max seed bonus: 45 pts
        win_score = stats["wins"] * 1.0              # each win = 1 pt
        offense_score = stats["ppg"] * 0.5           # each PPG = 0.5 pts
        defense_score = (100 - stats["oppg"]) * 0.5  # lower OPPG = better defense

        total = seed_score + win_score + offense_score + defense_score
        return round(total, 2)

    def predict_winner(self, team1_name: str, team2_name: str) -> dict:
        """
        Predict the winner of a matchup between two teams.

        Args:
            team1_name: Name of the first team.
            team2_name: Name of the second team.

        Returns:
            A dictionary containing:
                - winner: Name of the predicted winner
                - loser: Name of the predicted loser
                - confidence: Score difference between the two teams
                - explanation: Human-readable reasoning string
                - team1_score: Composite score for team 1
                - team2_score: Composite score for team 2
        """
        team1 = self.get_team_stats(team1_name)
        team2 = self.get_team_stats(team2_name)

        score1 = self._compute_score(team1)
        score2 = self._compute_score(team2)

        if score1 >= score2:
            winner, loser = team1, team2
            winner_score, loser_score = score1, score2
        else:
            winner, loser = team2, team1
            winner_score, loser_score = score2, score1

        confidence = round(winner_score - loser_score, 2)

        explanation = (
            f"{winner['team']} (#{int(winner['seed'])} seed) is predicted to beat "
            f"{loser['team']} (#{int(loser['seed'])} seed).\n"
            f"\n"
            f"  {winner['team']} stats:  {int(winner['wins'])}-{int(winner['losses'])} record, "
            f"{winner['ppg']} PPG, {winner['oppg']} OPPG  [Score: {winner_score}]\n"
            f"  {loser['team']} stats:   {int(loser['wins'])}-{int(loser['losses'])} record, "
            f"{loser['ppg']} PPG, {loser['oppg']} OPPG  [Score: {loser_score}]\n"
            f"\n"
            f"  Confidence margin: {confidence} points\n"
        )

        if confidence < 10:
            explanation += "  This is a very close matchup — could go either way!\n"
        elif confidence < 25:
            explanation += "  Moderate edge for the predicted winner.\n"
        else:
            explanation += "  Clear advantage for the predicted winner.\n"

        return {
            "winner": winner["team"],
            "loser": loser["team"],
            "confidence": confidence,
            "explanation": explanation,
            "team1_score": score1,
            "team2_score": score2,
        }
