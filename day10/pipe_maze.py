
possible_next = {
    "up"    : ["S", "|", "7", "F"],
    "down"  : ["S", "|", "L", "J"],
    "left"  : ["S", "-", "L", "F"],
    "right" : ["S", "-", "J", "7"]
}

'''
The pipes are arranged in a two-dimensional grid of tiles:

| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
'''

possible_outlets = {
    "S" : ["up", "down", "left", "right"],
    "|" : ["up", "down"],
    "-" : ["left", "right"],
    "L" : ["up", "right"],
    "J" : ["up", "left"],
    "7" : ["left", "down"],
    "F" : ["right", "down"]
}

ds = {
    "up"    : ( 0, -1),
    "down"  : ( 0,  1),
    "left"  : (-1,  0),
    "right" : ( 1,  0)
}

dir_to_symbol = {
    "up"    : "^",
    "down"  : "v",
    "left"  : "<",
    "right" : ">",
    "?" : "?",
}

def read_file(file):
    with open(file) as f:
        lines = f.readlines()
        lines = [line.strip("\n") for line in lines]

    maze = [[''] * (len(lines[0]) + 2)]

    for line in lines:
        maze.append(['.', *line, '.'])

    maze.append([[''] * (len(lines[0]) + 2)])

    return maze

def find_start(maze):
    for y, row in enumerate(maze) :
        for x, column in enumerate(row) :
            if column == "S" :
                return x, y

def find_next(pos, last_pos, maze):
    x, y = pos

    #Find which directions I can go, depending on my pipe part
    outlets = possible_outlets[maze[y][x]]

    next_positions = []
    for direction in outlets:
        # Find which parts would fit for my outlets
        possible_parts = possible_next[direction]

        # Find if there is a matching inlet
        dx, dy = ds[direction]
        if maze[y + dy][x + dx] in possible_parts :
            next_positions.append(((x + dx, y + dy), direction))

    # print(f"At ({x},{y}) next : {next_positions}")

    for pos, dir in next_positions :
        if pos == last_pos :
            next_positions.remove((pos, dir))

    if len(next_positions) == 1 or maze[y][x] == "S" :
        next_pos, direction = next_positions[0]
        nx, ny = next_pos
        if maze[ny][nx] == "S" :
            # print(f"Found the start!")
            return None, direction
        else :
            return ((nx, ny), direction)
    else :
        print("Error, found two (or more) paths")

def solve(file) :
    print(file)
    maze = read_file(file)

    start_pos = find_start(maze)
    pos = start_pos
    last_pos = pos
    at_start = False
    steps = 0
    visited_pos = [pos]
    directions = ["?"]
    while not at_start :
        next_pos, direction = find_next(pos, last_pos, maze)
        steps += 1
        if next_pos != start_pos :
            last_pos = pos
            pos = next_pos
            visited_pos.append(pos)
            directions.append(direction)
        else :
            print("Found start")
            directions[0] = direction
            break

    print(f"Part 1: {int(steps/2)} steps")

    # Part 2

    y_size = len(maze)
    x_size = len(maze[0])

    output_lines = []
    for y in range(y_size) :
        line = []
        for x in range(x_size):
            if (x, y) in visited_pos:
                index = visited_pos.index((x, y))
                dir = directions[index]

                line.append(dir_to_symbol[dir])
            else :
                line.append(".")
        output_lines.append(line)

    # Mark all spots in the inside. We are traveling counter clock wise.
    inside_ds = {
        'v' : [( 1,  0)],
        '^' : [(-1,  0)],
        '<' : [( 0,  1)],
        '>' : [( 0, -1)]
    }

    # Mark all spots in the inside. We are traveling counter clock wise.
    # inside_ds = {
    #     '^' : [( 1,  0)], # ( 1,  1)],
    #     'v' : [(-1,  0)], # (-1, -1)],
    #     '>' : [( 0,  1)], # ( 1,  1)],
    #     '<' : [( 0, -1)], # (-1, -1)]
    # }

    for y, _ in enumerate(output_lines) :
        for x, _ in enumerate(line):
            try:
                ds = inside_ds[output_lines[y][x]]
            except KeyError:
                ds = []

            if len(ds) > 0 :
                for dx, dy in ds :
                    if output_lines[y + dy][x + dx] == '.' :
                        output_lines[y + dy][x + dx] = 'o'


    # Fill the area around all 'o'
    for y, line in enumerate(output_lines) :
        for x, c in enumerate(line):
            if output_lines[y][x] == 'o' :
                for dx, dy in [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)] :
                    if output_lines[y + dy][x + dx] == '.' :
                        output_lines[y + dy][x + dx] = 'o'

    # Count all the 'o'
    total = 0
    for line in output_lines :
        for c in line:
            if c == 'o' :
                total += 1

    for line in output_lines :
        print(''.join(line))

    print(f"Part 2 : {total / 4}")
    print('491 is to low!!')
    print('')


def main():
    files = [
        # "day10/example",
        # "day10/example2",
        # "day10/example3",
        # "day10/example4",
        # "day10/example6",
        # "day10/example5",
        "day10/input",
        # "day10/henrik.txt",
        # "day10/andreas",
    ]

    for file in files:
        solve(file)

if __name__ == '__main__' :
    main()

# Henrik 567
# Lunkan 471
# Jag borde få 495
