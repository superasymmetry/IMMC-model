# Our mapping list
mapping = [5, 2, 0, 17, 18, 19, 13, 11, 10, 14, 6, 3, 15, 9, 8, 16, 1, 4, 12, 7]

# Original groupings
groupings = [
            [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15],[16,17,18,19]],
            [[0,5,10,15],[4,9,14,19],[8,13,18,3],[12,17,2,7],[16,1,6,11]],
            [[0,9,18,7],[4,13,2,11],[8,17,6,15],[12,1,10,19],[16,5,14,3]],
            [[0,13,6,19],[4,17,10,3],[8,1,14,7],[12,5,18,11],[16,9,2,15]],
            [[0,17,14,11],[4,1,18,15],[8,5,2,19],[12,9,6,3],[16,13,10,7]],
            [[0,4,8,12,16],[1,5,9,13,17],[2,6,10,14,18],[3,7,11,15,19]]
            ]

# Function to map a single group using our mapping list
def map_group(group):
    return [mapping[x] for x in group]

# Now, apply the mapping to all groups:
new_groupings = []
for round_group in groupings:
    new_round = []
    for group in round_group:
        new_round.append(map_group(group))
    new_groupings.append(new_round)

# Print the new groupings:
for r, round_group in enumerate(new_groupings):
    print(f"Round {r+1}:")
    for group in round_group:
        print(group)
