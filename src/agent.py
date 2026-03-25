from tools.stats_tool import get_team_stats
from decision import decide_winner


class MarchMadnessAgent:
    def __init__(self):
        pass

    def predict_matchup(self, team1, team2):
        # Step 1: retrieve data
        stats1 = get_team_stats(team1)
        stats2 = get_team_stats(team2)

        if stats1 is None or stats2 is None:
            raise ValueError("Could not retrieve team data.")

        # Step 2: decide winner
        winner = decide_winner(stats1, stats2)

        return winner

