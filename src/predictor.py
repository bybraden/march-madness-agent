import difflib
import pandas as pd


class MarchMadnessAgent:
    def __init__(self, csv_path: str):
        self.data = pd.read_csv(csv_path)

        # Normalize numeric columns if they exist
        numeric_cols = [
            "seed",
            "wins",
            "losses",
            "ppg",
            "oppg",
            "point_diff",
            "win_pct",
            "last10_wins",
            "sos",
        ]
        for col in numeric_cols:
            if col in self.data.columns:
                self.data[col] = pd.to_numeric(self.data[col], errors="coerce")

    def get_team_stats(self, team_name: str):
        normalized_input = team_name.strip().lower()

        # Common aliases
        aliases = {
            "uconn": "UConn",
            "u conn": "UConn",
            "st johns": "St. John's",
            "st. johns": "St. John's",
            "saint johns": "St. John's",
            "saint john's": "St. John's",
            "st john's": "St. John's",
            "michigan st": "Michigan State",
            "msu": "Michigan State",
            "iowa st": "Iowa State",
        }

        if normalized_input in aliases:
            canonical = aliases[normalized_input]
            exact_alias = self.data[
                self.data["team"].str.strip().str.lower() == canonical.strip().lower()
            ]
            if not exact_alias.empty:
                return exact_alias.iloc[0]

        # 1) Exact match first
        exact = self.data[
            self.data["team"].str.strip().str.lower() == normalized_input
        ]
        if not exact.empty:
            return exact.iloc[0]

        # 2) Startswith match for short names like "iowa state"
        startswith = self.data[
            self.data["team"].str.strip().str.lower().str.startswith(normalized_input)
        ]
        if len(startswith) == 1:
            return startswith.iloc[0]

        # 3) Fuzzy match only if exact failed
        team_names = self.data["team"].tolist()
        close = difflib.get_close_matches(team_name, team_names, n=1, cutoff=0.82)
        if close:
            matched = self.data[self.data["team"] == close[0]]
            if not matched.empty:
                return matched.iloc[0]

        return None

    def calculate_score(self, team):
        seed = team["seed"]
        wins = team["wins"]
        losses = team["losses"]
        ppg = team["ppg"]
        oppg = team["oppg"]

        games_played = wins + losses
        win_pct = (
            team["win_pct"]
            if "win_pct" in team.index and pd.notna(team["win_pct"])
            else wins / games_played
        )
        point_diff = (
            team["point_diff"]
            if "point_diff" in team.index and pd.notna(team["point_diff"])
            else ppg - oppg
        )
        last10_wins = (
            team["last10_wins"]
            if "last10_wins" in team.index and pd.notna(team["last10_wins"])
            else 7
        )
        sos = (
            team["sos"]
            if "sos" in team.index and pd.notna(team["sos"])
            else 5
        )

        # More balanced formula so seed does not dominate
        score = (
            (17 - seed) * 1.5      # seed matters, but less
            + win_pct * 40         # overall quality
            + point_diff * 3       # scoring margin
            + last10_wins * 2      # recent form
            + sos * 1.5            # schedule quality
        )

        return round(score, 2)

    def predict_winner(self, team1_name: str, team2_name: str):
        team1 = self.get_team_stats(team1_name)
        team2 = self.get_team_stats(team2_name)

        if team1 is None:
            raise ValueError(f"Team '{team1_name}' not found.")
        if team2 is None:
            raise ValueError(f"Team '{team2_name}' not found.")

        score1 = self.calculate_score(team1)
        score2 = self.calculate_score(team2)

        if score1 >= score2:
            winner = team1["team"]
            loser = team2["team"]
            winner_stats = team1
            loser_stats = team2
            confidence = round(score1 - score2, 2)
        else:
            winner = team2["team"]
            loser = team1["team"]
            winner_stats = team2
            loser_stats = team1
            confidence = round(score2 - score1, 2)

        explanation = (
            f"{winner} (#{int(winner_stats['seed'])} seed) is predicted to beat "
            f"{loser} (#{int(loser_stats['seed'])} seed).\n\n"
            f"{winner} stats: {int(winner_stats['wins'])}-{int(winner_stats['losses'])} record, "
            f"{winner_stats['ppg']:.1f} PPG, {winner_stats['oppg']:.1f} OPPG "
            f"[Score: {max(score1, score2)}]\n"
            f"{loser} stats: {int(loser_stats['wins'])}-{int(loser_stats['losses'])} record, "
            f"{loser_stats['ppg']:.1f} PPG, {loser_stats['oppg']:.1f} OPPG "
            f"[Score: {min(score1, score2)}]\n\n"
            f"Confidence margin: {confidence} points\n"
        )

        if confidence >= 20:
            explanation += "Clear advantage for the predicted winner."
        elif confidence >= 10:
            explanation += "Moderate edge for the predicted winner."
        else:
            explanation += "This is a very close matchup — could go either way!"

        return {
            "winner": winner,
            "loser": loser,
            "confidence": confidence,
            "explanation": explanation,
            "team1_score": score1,
            "team2_score": score2,
        }
