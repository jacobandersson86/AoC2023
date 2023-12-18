import itertools

def read_data(file) :
    with open(file) as f :
        lines = f.readlines()

    direction, length, color = [], [], []
    for line in lines:
        d, l, c = line.strip('\n').split(' ')
        direction.append(d)
        length.append(int(l))
        color.append(c)

    return direction, length, color

dir_ds = {
    "R" : (1, 0),
    "L" : (-1, 0),
    "D" : (0, 1), # +1 eventhough down since matrix is growing downward.
    "U" : (0, -1),
}

def calculate_positions(directions, lengths) :
    positions = [(1, 1)]
    for dir, l in zip(directions, lengths) :
        ds = dir_ds[dir]

        last_pos = positions[-1]

        for _ in range(l):
            lx, ly  = last_pos
            dx, dy = ds
            x, y = lx + dx, ly + dy
            positions.append((x, y))
            last_pos = (x, y)

    return positions

def print_map(dig_map) :
    for row in dig_map :
        print(''.join([c for c in row]))

def mark_plan(dig_map, positions, offset):
    dx, dy = offset
    for x, y in positions:
        dig_map[y + dy][x + dx] = '#'
    return dig_map

def flood_fill(dig_map, start, token) :
    # Fill the area around all 'token'
    positions = set([start])
    while len(positions) :
        new_positions = []
        removable = []
        for x, y in positions:
            if dig_map[y][x] == token :
                # Draw on this position
                dig_map[y][x] = 'o'
                # Find sorounding pos
                for dx, dy in [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)] :
                    nx, ny = x + dx, y + dy
                    # Check inside of map
                    if (nx >= 0 and nx < len(dig_map[0])) and (ny >= 0 and ny < len(dig_map)) :
                        # Check not the actual position
                        if not (nx == x and ny == y) :
                            # Add to next search
                            new_positions.append((nx, ny))
            removable.append((x, y))
        for r in removable :
            positions.remove(r)
        positions.update(new_positions)

    return dig_map

def find_grid_size(positions) :
    all_x, all_y = zip(*positions)
    min_x, min_y = min(all_x), min(all_y)
    max_x, max_y = max(all_x), max(all_y)

    offset = (abs(min_x) + 1, abs(min_y) + 1)
    size_x, size_y = (max_x - min_x), (max_y - min_y)

    return (size_x + 1 + 2, size_y + 1 + 2), offset

def count_dig_area(dig_map, tokens) :
    count = 0
    for x in range(len(dig_map[0])) :
        for y in range(len(dig_map)) :
            token = dig_map[y][x]
            if token in tokens :
                count += 1
    return count


def main() :
    directions, lengths, _ = read_data("day18/input")

    positions = calculate_positions(directions, lengths)

    (size_x, size_y), offset = find_grid_size(positions)

    dig_map = [['.' for _ in range(size_x)] for _ in range(size_y)]
    dig_map = mark_plan(dig_map, positions, offset)


    dig_map = flood_fill(dig_map,(0, 0), '.')
    area = count_dig_area(dig_map, set(['#', '.']))

    print_map(dig_map)
    print(f"Part 1 : {area}")

if __name__ == '__main__' :
    main()
