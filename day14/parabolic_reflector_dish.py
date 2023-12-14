
def roll_the_rocks(rock_line : str) :

    last_was_square_rock = True
    rock_sack = []
    fault_lines = []
    for i, c in enumerate(rock_line):
        if c == "#":
            last_was_square_rock = True
        if c == "O" or c == "." :
            if last_was_square_rock :
                last_was_square_rock = False
                fault_lines.append(i)
                rock_sack.append(0)
        if c == "O":
            rock_sack[-1] += 1

    fault_lines.append(len(rock_line) + 1)

    new_rock_line = ""
    for rocks, fault_line, next_line in zip(rock_sack, fault_lines, fault_lines[1:]) :
        length = next_line - fault_line
        if fault_line != 0 :
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
