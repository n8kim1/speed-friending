# TODO real test cases
# TODO parse input

group_size = 3

section_1 = set(["A1", "A2", "A3"])
section_2 = set(["B1", "B2", "B3"])
# TODO check if there's intersection, which would indicate something went wrong 

# Dict representing how much each person has been paired with another
# TODO gen on the fly, from input parsing
pair_freqs = dict()
pair_freqs["A1"] = {"B1": 0, "B2": 1, "B3": 1, "A2": 0, "A3": 0}
pair_freqs["A2"] = {"B1": 0, "B2": 1, "B3": 1, "A1": 0, "A3": 0}
pair_freqs["A3"] = {"B1": 1, "B2": 1, "B3": 1, "A1": 0, "A2": 0}
pair_freqs["B1"] = {"B2": 0, "B3": 0, "A1": 0, "A2": 0, "A3": 1}
pair_freqs["B2"] = {"B1": 0, "B3": 0, "A1": 1, "A2": 1, "A3": 1}
pair_freqs["B3"] = {"B1": 0, "B2": 0, "A1": 1, "A2": 1, "A3": 1}

# pair section 1 with section 2, if possible
# TODO dynamically count this
# TODO include downward scaling
pairing_counts = dict()
# (section1, section2)
for a in section_1:
    pairing_counts[a] = sum([pair_freqs[a][b] for b in pair_freqs[a] if b in section_2])

pairing_order = sorted(pairing_counts.keys(), key=lambda key: pairing_counts[key], reverse=True)

paired_this_round = []

def viable_to_group(person):
    for group in paired_this_round:
        if person in group and len(group) >= group_size:
            return False
    return True

def add_to_group(a, b):
    for group in paired_this_round:
        if a in group:
            group.add(b)
            return
        elif b in group:
            group.add(a)
            return
    paired_this_round.append(set((a, b)))

# pick a member of section 1, find a viable pair
for a in pairing_order:
    a_paired_with = None
    for b in sorted(pair_freqs[a].keys(), key=lambda b: pair_freqs[a][b]):
        if b in section_2 and viable_to_group(b):
            a_paired_with = b
            break
    if a_paired_with is not None:
        add_to_group(b, a)
        print(a, b)

print(paired_this_round)

# TODO handle extra ppl in section A
# TODO handle extra ppl in section B
# TODO save to output
