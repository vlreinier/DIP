from itertools import combinations

def listCombinations(all_columns):
    return [list(x) for i in range(1, len(all_columns)+1) for x in combinations(all_columns, i)]
