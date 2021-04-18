# TODO real test cases

import csv
import math
import random

# TODO >2 groups are problematic, esp w alg as written... see other comments for more
group_size = 4
# When enabled, will randomize the order in which people in section A are matched.
# Use sparingly to avoid undesired behavior, eg cycles in pairing
random_priority = False
if group_size>2:
    random_priority=True

# TODO take variable file name as cl input
# note: when processing names, we remove extra whitespace, to be safe
# caution: will cause "a b" and "ab" to be treated the same, for example
# TODO should be caps insensitive too
with open('input_example.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    # TODO strip whitespace in one go, to start
    # TODO include stripping empty / whitespace-only rows

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
                # Only interested in prior matches between 
                # people we're looking to pair _this round_.
                if i != j and i in all_people and j in all_people:
                    pair_freqs[i][j] += 1

paired_this_round = []

# some helper functions
def is_in_group(person):
    for group in paired_this_round:
        if person in group:
            return True
    return False

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

def get_group_size(a):
    for group in paired_this_round:
        if a in group:
            return len(group)
    return 0

def add_to_group(a, b):
    pair_freqs[a][b] += 1
    pair_freqs[b][a] += 1
    if is_in_group(a):
        if is_in_group(b):
            print("combining....")
            for group in paired_this_round:
                if a in group:
                    a_group = group
                    paired_this_round.remove(group)
            for group in paired_this_round:
                if b in group:
                    b_group = group
                    paired_this_round.remove(group)
            combined_group = a_group|b_group
            paired_this_round.append(combined_group)
            
        else:
            for group in paired_this_round:
                if a in group:
                    group.add(b)
    else:
        if is_in_group(b):
            for group in paired_this_round:
                if b in group:
                    group.add(a)
        else:
            paired_this_round.append(set((a, b)))
    return

# main loop of code, iterating and creating pairs
is_new_pair_created = True
while is_new_pair_created:
    is_new_pair_created = False
    # pair section 1 with section 2, if possible

    # Figure out the order in which to pick section 1.
    # Here, we define this order as imbalance in pairing:
    # roughly, the more a person in section 1 has not been paired with a particular person in section 2, 
    # and the more they have been paired with others in section 2, the more imbalanced.
    # They are perfectly balanced if they have met everyone in section 2 an equal number of times.
    pairing_priority = dict()
    for a in section_1:
        pair_counts_bipartite = [pair_freqs[a][b] for b in pair_freqs[a] if b in section_2]

        # Without the following: new people in section 1 will have priority zero,
        # and others will be paired before them. They will stay at priority zero for a while...
        # While this is fine and generally evens out after a while,
        # I'd prefer pairing the new people quicker.
        if sum(pair_counts_bipartite) == 0:
            # gives new people max priority
            pairing_priority[a] = math.inf
        else:
            pair_counts_bipartite_shifted = [count-min(pair_counts_bipartite) for count in pair_counts_bipartite]
            pairing_priority[a] = sum(pair_counts_bipartite_shifted)

    pairing_order = sorted(pairing_priority.keys(), key=lambda key: ((pairing_priority[key], random.random())), reverse=True)
    if random_priority:
        print("Caution - random prioritization of section 1 on!")
        pairing_order = sorted(pairing_priority.keys(), key=lambda key: random.random(), reverse=True)
    # pick a member of section 1, find a viable pair
    for a in pairing_order:
        if viable_to_group(a):
            a_paired_with = None
            for b in sorted(pair_freqs[a].keys(), key=lambda b: (pair_freqs[a][b], random.random())):
                if b in section_2 and viable_to_group(b) and not in_same_group(a, b):
                    if not (is_in_group(a) and is_in_group(b) and get_group_size(a)+get_group_size(b)>group_size):
                        a_paired_with = b
                        break
            if a_paired_with is not None:
                add_to_group(b, a)
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

# TODO there's so much duped work / code / methods / etc
# Can strip down on repetition

# strip down the pair freqs, for convenience
pair_freqs_ungrouped = dict()
for i in ungrouped_this_round:
    pair_freqs_ungrouped[i] = dict()
    for j in ungrouped_this_round:
        if i != j:
            pair_freqs_ungrouped[i][j] = pair_freqs[i][j]

pairing_priority = dict()
for i in ungrouped_this_round:
    pairing_priority[i] = sum([pair_freqs_ungrouped[i][j] for j in pair_freqs_ungrouped[i]])

pairing_order = sorted(pairing_priority.keys(), key=lambda key: ((pairing_priority[key], random.random())), reverse=True)

is_new_pair_created = True
while is_new_pair_created:
    is_new_pair_created = False
    for a in pairing_order:
        if viable_to_group(a):
            a_paired_with = None
            for b in sorted(pair_freqs_ungrouped[a].keys(), key=lambda b: (pair_freqs_ungrouped[a][b], random.random())):
                if viable_to_group(b) and not in_same_group(a, b):
                    a_paired_with = b
                    break
            if a_paired_with is not None:
                add_to_group(b, a)
                is_new_pair_created = True
                break

# TODO URGENT TODO handle any stragglers

# print to stdout, and write to file
random.shuffle(paired_this_round)
# TODO use whatever input file name is set too
# TODO add option to write to a diff file
with open('input_example.csv', 'a') as output_file:
    output_file.write("\n")
    for i in range(len(paired_this_round)):
        group_printable = ", ".join(paired_this_round[i])
        print(f"Room {i+1}: {group_printable}")
        output_file.write("\n" + group_printable)
