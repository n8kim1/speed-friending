# TODO real test cases

import csv
import random

group_size = 3

# TODO take variable file name as cl input
# note: when processing names, we remove extra whitespace, to be safe
# caution: will cause "a b" and "ab" to be treated the same, for example
with open('input_example.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')

    row = reader.__next__()
    section_1 = set(person.strip() for person in row)
    row = reader.__next__()
    section_2 = set(person.strip() for person in row)

    # TODO check if there's intersection, which would indicate something went wrong 
    all_people = section_1 | section_2
    # Nested symmetric dict, counting how much each person has been paired with another
    pair_freqs = dict()
    for i in all_people:
        pair_freqs[i] = dict()
        for j in all_people:
            if i != j:
                pair_freqs[i][j] = 0

    for row in reader:
        group = set(person.strip() for person in row)
        for i in group:
            for j in group:
                if i != j:
                    pair_freqs[i][j] += 1

paired_this_round = []

# some helper functions
def viable_to_group(person):
    for group in paired_this_round:
        if person in group and len(group) >= group_size:
            return False
    return True

def in_same_group(a, b):
    for group in paired_this_round:
        if a in group and b in group:
            return True
    return False

def add_to_group(a, b):
    pair_freqs[a][b] += 1
    pair_freqs[b][a] += 1
    for group in paired_this_round:
        if a in group:
            group.add(b)
            return
        elif b in group:
            group.add(a)
            return
    paired_this_round.append(set((a, b)))

# main loop of code, iterating and creating pairs
is_new_pair_created = True
while is_new_pair_created:
    is_new_pair_created = False
    # pair section 1 with section 2, if possible
    # TODO dynamically count this
    # TODO include downward scaling
    pairing_priority = dict()
    # (section1, section2)
    for a in section_1:
        pairing_priority[a] = sum([pair_freqs[a][b] for b in pair_freqs[a] if b in section_2])

    pairing_order = sorted(pairing_priority.keys(), key=lambda key: ((pairing_priority[key], random.random())), reverse=True)

    # pick a member of section 1, find a viable pair
    for a in pairing_order:
        if viable_to_group(a):
            a_paired_with = None
            for b in sorted(pair_freqs[a].keys(), key=lambda b: (pair_freqs[a][b], random.random())):
                if b in section_2 and viable_to_group(b) and not in_same_group(a, b):
                    a_paired_with = b
                    break
            if a_paired_with is not None:
                add_to_group(b, a)
                print(a, b)
                is_new_pair_created = True
                break

# At this point, there may be ungrouped people
ungrouped_this_round = [i for i in all_people if not is_in_group(i)]

# **Ungrouped people will be either only in section A, or only in section B**.
# So, we don't have to bother with bipartitness.
# (seeing this uses a proof by contradiction argument similar to stable matching;
# basically, if this wasn't true, a pair of people from A and B
# would have been attempted to match, and there's no reason they shouldn't have been paired.) 

# Grouping them is somewhat similar as before, though not bipartite:
# Considering groupings only within ungrouped people,
# find the most unbalanced, and pair the most unbalanced 
# according to who they have been least paired with.


# TODO handle extra ppl in section A
# TODO handle extra ppl in section B
# TODO save to output
