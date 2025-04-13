import math
import numpy as np
import random

# Initialize teams with rankings 0-19 (higher rank = stronger)
teams = list(range(20))  

# Assign skills inversely to ranking (e.g., Team 0 is best)
team_skills = {team: 100 - team * 2 for team in teams}  # Higher rank = lower number
team_records = {team: {'wins': 0, 'losses': 0} for team in teams}

def expected_win_prob(skill_A, skill_B):
    """Computes probability of team A winning against team B."""
    return skill_A / (skill_A + skill_B)

def simulate_match(team_A, team_B):
    """Simulates a match based on skill levels and updates team records."""
    prob_A_wins = expected_win_prob(team_skills[team_A], team_skills[team_B])
    winner = team_A if random.random() < prob_A_wins else team_B
    
    # Update win/loss records
    if winner == team_A:
        team_records[team_A]['wins'] += 1
        team_records[team_B]['losses'] += 1
    else:
        team_records[team_B]['wins'] += 1
        team_records[team_A]['losses'] += 1

    return winner

def poisson_schedule(teams, T=50, lambda_matches=0.5):
    """Schedules matches using a Poisson process for a single round-robin tournament."""
    matches = [(team1, team2) for i, team1 in enumerate(teams) for team2 in teams[i+1:]]
    num_matches = len(matches)

    # Generate Poisson interarrival times
    interarrivals = np.random.exponential(scale=1/lambda_matches, size=num_matches)
    match_times = np.cumsum(interarrivals)
    match_times = (match_times / match_times[-1]) * T  # Normalize times to fit within T

    random.shuffle(matches)  # Randomize match order

    schedule = []
    for time, (team_A, team_B) in zip(match_times, matches):
        winner = simulate_match(team_A, team_B)
        schedule.append((round(time), team_A, team_B, winner))

    return schedule

def rank_teams():
    """Prints team rankings based on wins and losses."""
    sorted_teams = sorted(team_records.items(), key=lambda x: (-x[1]['wins'], x[1]['losses']))
    
    print("\n🏆 **Final Rankings** 🏆")
    print("{:<5} {:<10} {:<10} {:<10}".format("Rank", "Team", "Wins", "Losses"))
    for rank, (team, record) in enumerate(sorted_teams, start=1):
        print(f"{rank:<5} {team:<10} {record['wins']:<10} {record['losses']:<10}")

def simulate_poisson_round_robin():
    """Runs the Poisson process tournament and prints match results and rankings."""
    schedule = poisson_schedule(teams, T=50, lambda_matches=0.5)

    # Print the match schedule
    print("\n📅 **Match Schedule and Results** 📅")
    for match in schedule:
        print(f"Day {match[0]}: Team {match[1]} vs Team {match[2]} - 🏆 Winner: Team {match[3]}")

    # Print final rankings
    rank_teams()

# Run Poisson Round-Robin Simulation
simulate_poisson_round_robin()
