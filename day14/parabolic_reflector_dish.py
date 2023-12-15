from input import input

example = [
    "O....#....",
    "O.OO#....#",
    ".....##...",
    "OO.#O....O",
    ".O.....O#.",
    "O.#..O.#.#",
    "..O..#O..O",
    ".......O..",
    "#....###..",
    "#OO..#....",
]

def transpose(patch):
    height = len(patch)
    transposed_patch = []
    for column in reversed(range(len(patch[0]))) :
        line = ''.join([patch[row][column] for row in range(height)])
        transposed_patch.append(line)

    return transposed_patch

def roll_the_rocks(rock_line : str) :

    last_was_square_rock = True
    rock_sack = [0]
    square_rocks = [-1]
    for i, c in enumerate(rock_line):
        if c == "#":
            square_rocks.append(i)
            last_was_square_rock = True
            rock_sack.append(0)
        if c == "O":
            rock_sack[-1] += 1
        if c == "O" or c == "." :
            if last_was_square_rock :
                last_was_square_rock = False

    square_rocks.append(len(rock_line))
    rock_sack.append(0)

    new_rock_line = ""
    for rocks, square_rock, next_square_rock in zip(rock_sack, square_rocks, square_rocks[1:]) :
        length = next_square_rock - square_rock
        if square_rock >= 0 :
            new_rock_line += "#"
        new_rock_line += "".join('O'*rocks) + "".join('.'*(length - rocks - 1))

    return new_rock_line

def weigh_the_rocks(rock_line : str) :
    max_weight = len(rock_line)
    weights = [max_weight - i for i, ch in enumerate(rock_line) if ch == 'O']
    return sum(weights)

def roll_and_weigh(patch) :
    weight = 0
    for i, rock_line in enumerate(patch) :
        new_line = roll_the_rocks(rock_line)
        weight += weigh_the_rocks(new_line)
        patch[i] = new_line
    return weight

def print_patch(patch):
    for line in patch:
        print(line)

def count_rocks(patch, rock_type) :
    count = 0
    for line in patch:
        count += line.count(rock_type)
    return count

def main() :

    # tests = [
    #     "....O...#...O.O..",
    #     "#.....O...",
    #     "#OO#.O",
    #     "....#O",
    #     "....#",
    #     "#....",
    #     "#...#",
    #     "....",
    #     "O...",
    #     "....O",
    # ]

    # for test in tests :
    #     print(test)
    #     print(len(test))
    #     print(roll_the_rocks(test))
    #     print(len(roll_the_rocks(test)))
    #     print(f"Weight {weigh_the_rocks(roll_the_rocks(test))}")
    #     print('')

    patch = input

    print(f"Before: '#' {count_rocks(patch, '#')}")
    print(f"Before: 'O' {count_rocks(patch, 'O')}")

    # print_patch(transpose(patch))

    print(hash(''.join([line for line in patch])))

    patch_set = dict()
    patch_naming = 0
    patch_names = dict()
    patch_weights = dict()
    patch_period = dict()
    patch_first_iteration = dict()
    for i in range(500) :
        # Turn north towards west, because my scale is in west ;-)
        patch = transpose(patch)
        weight = roll_and_weigh(patch)
        patch_hash = hash(''.join([line for line in patch]))

        # if i == 0 :
        #     print(f"First patch at iteration {i}, weight {weight}")
        # print_patch(patch)
        # print(weight)
        # print('')
        if (patch_hash) in patch_set:
            if patch_hash not in patch_names :
                patch_names[patch_hash] = patch_naming
                patch_weights[patch_hash] = weight
                patch_period[patch_hash] = i - patch_set[patch_hash]
                patch_first_iteration[patch_hash] = patch_set[patch_hash]

                patch_naming += 1

            # print(f"Patch {patch_names[patch_hash]} found again at iteration {i}")
            # print(f"Previous was in iteration {patch_set[patch_hash]}")
            # print(f"The weight is {patch_weights[patch_hash]} and periodicity is {patch_period[patch_hash]}")



        patch_set[patch_hash] = i

    for key in patch_names.keys():
        print(f"Found {patch_names[key]} the first time at iteration {patch_first_iteration[key]}")
        print(f"The weight is {patch_weights[key]} and periodicity is {patch_period[key]}")
        print('')


    print(f"After: '#' {count_rocks(patch, '#')}")
    print(f"After: 'O' {count_rocks(patch, 'O')}")


# 145782 is to high!
# 110374 is to high! (nr 50)
# 103162 is to high nr 49
# 102458 is not right

if __name__ == "__main__" :
    main()
