import pandas as pd

# Load datasets
players = pd.read_csv("dim_players_no_images.csv")
batting = pd.read_csv("fact_bating_summary.csv")
bowling = pd.read_csv("fact_bowling_summary.csv")

# -------------------------------
# Batting Analysis
# -------------------------------
batting["SR"] = pd.to_numeric(batting["SR"], errors="coerce")

batting_summary = (
    batting.groupby("batsmanName")
    .agg(
        Total_Runs=("runs", "sum"),
        Balls_Faced=("balls", "sum"),
        Innings=("match_id", "count"),
        Avg_Strike_Rate=("SR", "mean"),
        Fours=("4s", "sum"),
        Sixes=("6s", "sum"),
    )
    .reset_index()
)

batting_summary["Batting_Score"] = (
    batting_summary["Total_Runs"] * 0.5
    + batting_summary["Avg_Strike_Rate"] * 0.3
    + batting_summary["Sixes"] * 2
)

# -------------------------------
# Bowling Analysis
# -------------------------------
bowling_summary = (
    bowling.groupby("bowlerName")
    .agg(
        Wickets=("wickets", "sum"),
        Economy=("economy", "mean"),
        Maidens=("maiden", "sum"),
        Dot_Balls=("0s", "sum"),
    )
    .reset_index()
)

bowling_summary["Bowling_Score"] = (
    bowling_summary["Wickets"] * 10
    - bowling_summary["Economy"] * 2
    + bowling_summary["Dot_Balls"] * 0.2
)

# -------------------------------
# Merge Player Information
# -------------------------------
batting_final = batting_summary.merge(
    players,
    left_on="batsmanName",
    right_on="name",
    how="left"
)

bowling_final = bowling_summary.merge(
    players,
    left_on="bowlerName",
    right_on="name",
    how="left"
)

# -------------------------------
# Select Dream Team
# -------------------------------

top_batters = batting_final.sort_values(
    by="Batting_Score",
    ascending=False
).head(6)

top_bowlers = bowling_final.sort_values(
    by="Bowling_Score",
    ascending=False
).head(4)

all_rounders = batting_final[
    batting_final["playingRole"].str.contains(
        "Allrounder",
        case=False,
        na=False
    )
].sort_values(
    by="Batting_Score",
    ascending=False
).head(1)

dream_team = pd.concat([
    top_batters,
    all_rounders
])

print("\nTOP BATTERS")
print(top_batters[
    ["batsmanName", "Total_Runs", "Avg_Strike_Rate", "Batting_Score"]
])

print("\nTOP BOWLERS")
print(top_bowlers[
    ["bowlerName", "Wickets", "Economy", "Bowling_Score"]
])

print("\nALL-ROUNDER")
print(all_rounders[
    ["batsmanName", "playingRole", "Batting_Score"]
])

print("\nDREAM TEAM")
print(dream_team[
    ["batsmanName", "team", "playingRole"]
])

# Save outputs
top_batters.to_csv("top_batters.csv", index=False)
top_bowlers.to_csv("top_bowlers.csv", index=False)
dream_team.to_csv("dream_team.csv", index=False)

print("\nFiles Generated:")
print("1. top_batters.csv")
print("2. top_bowlers.csv")
print("3. dream_team.csv")
