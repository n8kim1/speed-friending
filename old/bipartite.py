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