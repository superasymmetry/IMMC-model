import itertools

# All 24 letters
letters = list("ABCDEFGHIJKLMNOPQRSTUVWX")

# Your 24 existing groups of 4 (from the screenshot), grouped by columns:
existing_groups = [
    ["AFKP","BGLM","CHIN","DEJO"],
    ["QVAG","RWBH","SXCE","TUDF"],
    ["IOQW","JPRX","KMSU","LNTV"],
    ["ALSB","BITC","CJQD","DKRA"],
    ["ITAH","JQBE","KRCF","LSDG"],
    ["KNQX","LORU","IPSV","JMTW"],
]

# 1) Build a set of ALL 276 possible pairs (24 choose 2)
all_pairs = set(itertools.combinations(letters, 2))

# 2) Remove any pair already appearing in the existing groups
for col in existing_groups:
    for group_of_4 in col:
        # Each group_of_4 is something like "AFKP"
        for pair in itertools.combinations(group_of_4, 2):
            sorted_pair = tuple(sorted(pair))
            if sorted_pair in all_pairs:
                all_pairs.remove(sorted_pair)

print("Number of pairs covered by original groups:", 276 - len(all_pairs))
print("Number of leftover (unplayed) pairs:", len(all_pairs))

leftover_pairs = list(all_pairs)
unused = set(leftover_pairs)  # pairs not yet placed in a new group
new_groups = []               # each group is a set of letters

while unused:
    # Start a new group with one leftover pair
    group_pairs = []
    group_letters = set()

    seed = unused.pop()
    group_pairs.append(seed)
    group_letters.update(seed)

    # Try to add more leftover pairs to this group
    # as long as we don't exceed 6 letters total
    to_remove = []
    for pair in list(unused):
        a, b = pair
        # We can add this pair if it does not share a letter already in the group
        # OR if the group can still expand without repeating any pair
        # but we want all pairs in the group to be disjoint from existing group letters
        # so that we don't accidentally place the same pair in two groups
        if a not in group_letters and b not in group_letters:
            # check if adding them keeps group size <= 6
            if len(group_letters) + 2 <= 6:
                group_pairs.append(pair)
                group_letters.update([a,b])
                to_remove.append(pair)

    # Remove all pairs we placed from the unused set
    for p in to_remove:
        unused.remove(p)

    new_groups.append(sorted(group_letters))

# Show the final new groups
print("\nNew Groups to Cover All Leftover Pairs (no repeats):\n")
for i, grp in enumerate(new_groups, start=1):
    print(f"Group {i}: {' '.join(grp)}")
