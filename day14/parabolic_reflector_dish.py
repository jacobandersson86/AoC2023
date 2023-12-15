
def roll_the_rocks(rock_line : str) :

    last_was_square_rock = True
    rock_sack = [0]
    square_rocks = [-1]
    for i, c in enumerate(rock_line):
        if c == "#":
            square_rocks.append(i)
            last_was_square_rock = True
        if c == "O" or c == "." :
            if last_was_square_rock :
                last_was_square_rock = False
                rock_sack.append(0)
        if c == "O":
            rock_sack[-1] += 1

    square_rocks.append(len(rock_line))
    rock_sack.append(0)

    new_rock_line = ""
    for rocks, square_rock, next_square_rock in zip(rock_sack, square_rocks, square_rocks[1:]) :
        length = next_square_rock - square_rock
        if square_rock >= 0 :
            new_rock_line += "#"
        new_rock_line += "".join('O'*rocks) + "".join('.'*(length - rocks - 1))

    return new_rock_line


def main() :

    tests = [
        "....O...#...O.O..",
        "#.....O...",
        "#OO#.O",
        "....#O",
        "....#",
        "#....",
        "#...#",
        "....",
        "O...",
        "....O",
    ]

    for test in tests :
        print(test)
        print(len(test))
        print(roll_the_rocks(test))
        print(len(roll_the_rocks(test)))
        print('')




if __name__ == "__main__" :
    main()
