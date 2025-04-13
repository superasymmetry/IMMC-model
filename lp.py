import pulp
import math

# Example data:
teams = list(range(8))  # for 8 teams
num_teams = len(teams)
rounds = num_teams - 1  # single round-robin: (n-1) rounds

# Example: Travel distance matrix between teams' home venues (in km)
# (In practice, you could compute this using great-circle distance from team_locations.)
distance = {}
for i in teams:
    for j in teams:
        if i != j:
            # Here we use a dummy function for distance. Replace with actual distances.
            distance[(i, j)] = abs(i - j) * 100  # for example purposes

# Create a LP minimization problem
model = pulp.LpProblem("Tournament_Scheduling", pulp.LpMinimize)

# Decision variables: x[i,j,r] = 1 if team i plays at team j's venue in round r.
# (This is one possible formulation for scheduling the matches.)
x = pulp.LpVariable.dicts("x", 
                          ((i, j, r) for i in teams for j in teams if i != j for r in range(rounds)),
                          cat="Binary")

# Objective: minimize total travel distance.
# Assume that if team i plays at team j's venue, team i must travel distance[i,j].
model += pulp.lpSum(distance[(i, j)] * x[(i, j, r)]
                    for i in teams for j in teams if i != j for r in range(rounds)), "TotalTravelDistance"

# Constraints:
# (1) Each team i must play exactly one match in each round.
for i in teams:
    for r in range(rounds):
        model += pulp.lpSum(x[(i, j, r)] for j in teams if i != j) == 1, f"OneMatchPerRound_Team_{i}_Round_{r}"

# (2) Each pair of teams i and j play exactly once (ignoring home/away order for now).
for i in teams:
    for j in teams:
        if i < j:
            model += pulp.lpSum(x[(i, j, r)] + x[(j, i, r)] for r in range(rounds)) == 1, f"MatchOnce_{i}_{j}"

# (3) Additional constraints can be added here (home-away balance, venue availability, etc.)

# Solve the model
solver = pulp.PULP_CBC_CMD()  # or choose another solver
model.solve(solver)

print("Status:", pulp.LpStatus[model.status])
print("Total Travel Distance:", pulp.value(model.objective()))

# Retrieve the schedule:
schedule = {}
for r in range(rounds):
    schedule[r] = []
    for i in teams:
        for j in teams:
            if i != j and pulp.value(x[(i, j, r)]) == 1:
                schedule[r].append((i, j))
print("Schedule by rounds:")
for r in schedule:
    print(f"Round {r+1}: {schedule[r]}")
