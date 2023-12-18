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

def calculate_positions_line(directions, lengths) :
    positions = [(0, 0)]
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

def calculate_positions(directions, lengths) :
    positions = [(0, 0)]
    for dir, l in zip(directions, lengths) :
        ds = dir_ds[dir]

        last_pos = positions[-1]
        lx, ly  = last_pos

        dx, dy = ds
        x, y = lx + dx * l, ly + dy * l

        positions.append((x, y))

    return positions

def area_by_shoelace(points):
    x, y = zip(*points)
    "Assumes x,y points go around the polygon in one direction"
    return abs( sum(i * j for i, j in zip(x,             y[1:] + y[:1]))
               -sum(i * j for i, j in zip(x[1:] + x[:1], y            ))) / 2

# def border_area(directions, lengths) :
#     return len(calculate_positions_line(directions, lengths))

def print_map(dig_map) :
    for row in dig_map :
        print(''.join([c for c in row]))

def mark_plan(dig_map, positions, offset, token):
    dx, dy = offset
    for x, y in positions:
        dig_map[y + dy][x + dx] = token
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

color_to_dir = {
    "0" : 'R',
    '1' : 'D',
    '2' : 'L',
    '3' : 'U'
}

def color_to_instructions(colors):
    directions, lengths = [], []
    for color in colors:
        dir = color[-2]
        length = color[2:-2]

        directions.append(color_to_dir[dir])
        lengths.append(int(length, 16))
    return directions, lengths

def calculate_border_area(points) :
    length = 1
    for pos0, pos1 in zip(points[:],points[1:]) :
        x0, y0 = pos0
        x1, y1 = pos1
        dx = abs(x0 - x1)
        dy = abs(y0 - y1)
        length += dx + dy
    return (length + 1) / 2

def main() :
    directions, lengths, colors = read_data("day18/input")

    positions = calculate_positions_line(directions, lengths)

    (size_x, size_y), offset = find_grid_size(positions)

    dig_map = [['.' for _ in range(size_x)] for _ in range(size_y)]
    dig_map = mark_plan(dig_map, positions, offset, '*')


    dig_map = flood_fill(dig_map,(0, 0), '.')
    area = count_dig_area(dig_map, set(['#', '.', '*']))

    points = calculate_positions(directions, lengths)
    dig_map = mark_plan(dig_map, points, offset, '#')

    print_map(dig_map)
    print(f"Part 1 : {area}")

    ## Part 2. To big for flood fill. Let's use Shoe Lace

    directions, lengths = color_to_instructions(colors)

    points = calculate_positions(directions, lengths)
    border_area = calculate_border_area(points)

    area = area_by_shoelace(points)
    area += border_area
    print(f"Part 2 : {area}")


if __name__ == '__main__' :
    main()
