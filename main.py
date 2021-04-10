# TODO parse input

section_1 = set(["A1", "A2"])
section_2 = set(["B1", "B2"])

# TODO turn present matches into a better structure
# Dict of ppl not matched with?
# As example: A1 paired w B1, A2 w B2, already
possible_pairings = dict()
possible_pairings["A1"] = set("A2", "B2") 
possible_pairings["A2"] = set("A1", "B1") 
possible_pairings["B1"] = set("A2", "B2") 
possible_pairings["B2"] = set("A1", "B1") 

