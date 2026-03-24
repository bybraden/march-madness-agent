"""
March Madness Agent - Main Entry Point
Run this script to predict the winner of a March Madness matchup.

Usage:
    python src/main.py
"""

import os
import sys
from datetime import datetime

# Allow imports from the src directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from predictor import MarchMadnessAgent


def main():
    print("=" * 55)
    print("       🏀  March Madness Prediction Agent  🏀")
    print("=" * 55)

    # Resolve path to teams.csv relative to this file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "data", "teams.csv")
    output_path = os.path.join(base_dir, "outputs", "predictions.txt")

    # Load the agent
    try:
        agent = MarchMadnessAgent(csv_path)
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        sys.exit(1)

    print("\nAvailable teams:")
    for team in agent.data["team"].tolist():
        print(f"  - {team}")

    print()

    # Get team inputs
    team1 = input("Enter Team 1: ").strip()
    team2 = input("Enter Team 2: ").strip()

    print()

    # Run prediction
    try:
        result = agent.predict_winner(team1, team2)
    except ValueError as e:
        print(f"\nError: {e}")
        sys.exit(1)

    # Display result
    print("-" * 55)
    print(f"  🏆  Predicted Winner: {result['winner']}")
    print("-" * 55)
    print(result["explanation"])

    # Save result to file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(output_path, "a") as f:
        f.write("=" * 55 + "\n")
        f.write(f"Prediction Date: {timestamp}\n")
        f.write(f"Matchup: {team1} vs {team2}\n")
        f.write(f"Predicted Winner: {result['winner']}\n\n")
        f.write(result["explanation"])
        f.write("\n")

    print(f"Result saved to: {output_path}")
    print("=" * 55)


if __name__ == "__main__":
    main()
