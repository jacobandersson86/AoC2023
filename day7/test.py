from itertools import permutations

my_list = [1, 2, 3]

# Get all permutations
all_permutations = list(permutations(my_list))

# Get the number of permutations
num_permutations = len(all_permutations)

print(f"Total number of permutations: {num_permutations}")

