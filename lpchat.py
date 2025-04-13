import pulp
import math
import itertools

class SchedulerLP:
    def __init__(self, p_num):
        self.teams = [i for i in range(20)]  # 20 teams
        self.p_num = p_num
        self.weight = [0.3, 0.3, 0.4, 0.1]  # Adjusted weightings

        # Team locations (same as your dataset)
        self.team_locations = [
            (-25.274398, 133.775136), (37.09024, -95.712891), (23.634501, -102.552784),  # OC, NA
            (9.748917, -83.753428), (8.537981, -80.782127),  # CA
            (-38.416097, -63.616672), (-14.235004, -51.92528), (-32.522779, -55.765835), (4.570868, -74.297333),  # SA
            (46.603354, 1.888334), (40.463667, -3.74922), (52.132633, 5.291266), (55.378051, -3.435973), (39.399872, -8.224454),  # EU
            (31.791702, -7.09262), (14.497401, -14.452362),  # AF
            (36.204824, 138.252924), (14.058324, 108.277199), (32.427908, 53.688046), (38.963745, 35.243322)  # AS
        ]

        self.rounds = list(range(5))  # 5 rounds of matches (assuming single round-robin format)

        # Create a distance matrix based on travel cost function
        self.distances = self.compute_distance_matrix()

        # Define LP problem
        self.model = pulp.LpProblem("Tournament_Scheduling", pulp.LpMinimize)
        self.x = pulp.LpVariable.dicts("x", 
                                       ((i, j, r) for i in self.teams for j in self.teams if i < j for r in self.rounds),
                                       cat="Binary")

    def compute_distance_matrix(self):
        """Compute great-circle distances between all teams."""
        distances = {}
        for (i, loc1), (j, loc2) in itertools.combinations(enumerate(self.team_locations), 2):
            lat1, lon1 = loc1
            lat2, lon2 = loc2
            dist = 6371 * math.acos(math.sin(math.radians(lat1)) * math.sin(math.radians(lat2)) +
                                    math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
                                    math.cos(math.radians(lon2) - math.radians(lon1)))
            distances[(i, j)] = dist
        return distances

    def fairness(self, i, j):
        """Fairness function as variance of distances."""
        d = self.distances.get((i, j), self.distances.get((j, i), 0))
        return (d - sum(self.distances.values()) / len(self.distances)) ** 2

    def cost_fairness(self, i, j):
        """Variance of travel cost."""
        return self.fairness(i, j)

    def travelcost(self, i, j):
        """Travel cost function."""
        d = self.distances.get((i, j), self.distances.get((j, i), 0))
        return 65.87 + 0.23 * d + 3 * 100  # 3 nights stay

    def sus(self, i, j):
        """Sustainability function."""
        d = self.distances.get((i, j), self.distances.get((j, i), 0))
        return (d / 1000) * (0.8 ** (2 * math.log(d))) + 3 / 3

    def set_objective(self):
        """Define the objective function for LP."""
        self.model += pulp.lpSum(
            (self.weight[0] * self.fairness(i, j) +
             self.weight[1] * self.cost_fairness(i, j) +
             self.weight[2] * self.travelcost(i, j) +
             self.weight[3] * self.sus(i, j)) * self.x[i, j, r]
            for i in self.teams for j in self.teams if i < j for r in self.rounds
        )

    def set_constraints(self):
        """Define constraints to ensure valid tournament scheduling."""
        # Each team plays exactly once per round
        for i in self.teams:
            for r in self.rounds:
                self.model += pulp.lpSum(self.x[i, j, r] for j in self.teams if i < j) == 1, f"MatchPerRound_{i}_{r}"

        # Each team plays against every other team exactly once
        for i, j in self.distances.keys():
            self.model += pulp.lpSum(self.x[i, j, r] for r in self.rounds) == 1, f"OneMatch_{i}_{j}"

    def solve(self):
        """Solve the LP model."""
        self.set_objective()
        self.set_constraints()
        self.model.solve(pulp.PULP_CBC_CMD())

        print("Status:", pulp.LpStatus[self.model.status])
        print("Total Travel Distance:", pulp.value(self.model.objective))

        # Retrieve and print the final schedule
        schedule = {r: [] for r in self.rounds}
        for r in self.rounds:
            for i, j in self.distances.keys():
                if pulp.value(self.x[i, j, r]) == 1:
                    schedule[r].append((i, j))
        
        print("\nFinal Schedule by Rounds:")
        for r, matches in schedule.items():
            print(f"Round {r + 1}: {matches}")

        return schedule

# Running the LP Scheduler
scheduler_lp = SchedulerLP(20)
final_schedule = scheduler_lp.solve()
