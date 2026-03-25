def decide_winner(team1, team2):
    score1 = 0
    score2 = 0

    # Compare stats safely (skip if missing)

    if "ppg" in team1 and "ppg" in team2:
        if team1["ppg"] > team2["ppg"]:
            score1 += 1
        else:
            score2 += 1

    if "oppg" in team1 and "oppg" in team2:
        if team1["oppg"] < team2["oppg"]:  # lower is better
            score1 += 1
        else:
            score2 += 1

    if "win_pct" in team1 and "win_pct" in team2:
        if team1["win_pct"] > team2["win_pct"]:
            score1 += 1
        else:
            score2 += 1

    if "sos" in team1 and "sos" in team2:
        if team1["sos"] > team2["sos"]:
            score1 += 1
        else:
            score2 += 1

    if "ft_pct" in team1 and "ft_pct" in team2:
        if team1["ft_pct"] > team2["ft_pct"]:
            score1 += 1
        else:
            score2 += 1

    if "off_reb" in team1 and "off_reb" in team2:
        if team1["off_reb"] > team2["off_reb"]:
            score1 += 1
        else:
            score2 += 1

    if "def_reb" in team1 and "def_reb" in team2:
        if team1["def_reb"] > team2["def_reb"]:
            score1 += 1
        else:
            score2 += 1

    # Decide winner
    if score1 >= score2:
        return team1["team"]
    else:
        return team2["team"]

