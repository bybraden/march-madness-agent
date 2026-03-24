import pandas as pd
from predictor import MarchMadnessAgent


def load_matchups(path):
    return pd.read_csv(path)


def show_matchups(matchups):
    print("\nSweet 16 Matchups:")
    for i, row in matchups.iterrows():
        print(f"{row['game_id']}. {row['team1']} vs {row['team2']}")


def predict_one(agent, matchups):
    show_matchups(matchups)
    choice = input("\nEnter game number: ").strip()

    try:
        choice = int(choice)
        game = matchups[matchups["game_id"] == choice].iloc[0]
    except:
        print("Invalid selection.")
        return

    result = agent.predict_winner(game["team1"], game["team2"])
    print("\n" + result)


def predict_all(agent, matchups):
    print("\nPredictions for Sweet 16:\n")
    for _, game in matchups.iterrows():
        result = agent.predict_winner(game["team1"], game["team2"])
        print(result)
        print("-" * 50)


def main():
    agent = MarchMadnessAgent("data/teams.csv")
    matchups = load_matchups("data/sweet16_matchups.csv")

    while True:
        print("\n=== March Madness Agent ===")
        print("1. Show Sweet 16 matchups")
        print("2. Predict one game")
        print("3. Predict all games")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_matchups(matchups)
        elif choice == "2":
            predict_one(agent, matchups)
        elif choice == "3":
            predict_all(agent, matchups)
        elif choice == "4":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
