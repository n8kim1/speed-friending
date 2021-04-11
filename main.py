# TODO real test cases
# TODO parse input

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
        if person in group:
            return False
    return True

# pick a member of section 1, find a viable pair
for a in pairing_order:
    a_paired_with = None
    for b in section_2:
        # TODO just pick the next best person in Group 2, 
        # don't give up if all ppl a has never matched with don't have partner still
        if (b not in pair_freqs[a] or pair_freqs[a][b]==0) and viable_to_group(b):
            a_paired_with = b
            break
    if a_paired_with is not None:
        paired_this_round.append(set((a, b)))
        print(a, b)

# TODO handle extra ppl in section A
# TODO handle extra ppl in section B
# TODO save to output

# # TODO finish changing variable names, datatypes, etc
# # based on https://www.tuorialspoint.com/Maximum-Bipartite-Matching
# # A DFS based recursive function
# # that returns true if a matching 
# # for u, in section 1, is possible
# def bpm(self, u, matchR, seen):
#     # Try every member of section 2 one by one
#     for v in section_2:

#         # If u is available to match with 
#         # v and v is not seen
#         if v in possible_pairings[u] and v not in seen:
                
#             # Mark v as visited
#             seen.add(v) 

#             # If job 'v' is not assigned to
#             # an applicant OR previously assigned 
#             # applicant for job v (which is matchR[v]) 
#             # has an alternate job available. 
#             # Since v is marked as visited in the 
#             # above line, matchR[v]  in the following
#             # recursive call will not get job 'v' again
#             if matchR[v] == -1 or self.bpm(matchR[v], matchR, seen):
#                 matchR[v] = u
#                 return True
#     return False

# # Returns maximum number of matching 
# def maxBPM(self):
#     '''An array to keep track of the 
#         applicants assigned to jobs. 
#         The value of matchR[i] is the 
#         applicant number assigned to job i, 
#         the value -1 indicates nobody is assigned.'''
#     matchR = [-1] * self.jobs
        
#     # Count of jobs assigned to applicants
#     result = 0 
#     for i in range(self.ppl):
            
#         # Mark all jobs as not seen for next applicant.
#         seen_set = set()
            
#         # Find if the applicant 'u' can get a job
#         if self.bpm(i, matchR, seen):
#             result += 1
#     return result