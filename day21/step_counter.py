
def read_data(file):
    with open(file) as f:
        lines = f.readlines()

    garden = []
    for line in lines:
        garden.append([c for c in line.strip('\n')])

    return garden

def find_token(garden, token) :
    for y, line in enumerate(garden) :
        for x, c in enumerate(line) :
            if c == token :
                return (x, y)

def explore(garden, start, tokens, depth) :
    # Fill the area around all 'token'
    positions = set([start])

    even_steps = []
    odd_steps = []
    for i in range(depth + 1) :
        new_positions = []
        for x, y in positions:
            if any([garden[y][x] == token for token in tokens]):
                # This pos was accepted
                if i % 2 == 0 :
                    even_steps.append((x, y))
                else :
                    odd_steps.append((x, y))

                # Find sorounding pos
                for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)] :
                    nx, ny = x + dx, y + dy
                    # Check inside of map
                    if (nx >= 0 and nx < len(garden[0])) and (ny >= 0 and ny < len(garden)) :
                        # Check not the actual position
                        if not (nx == x and ny == y) :
                            # Add to next search
                            new_positions.append((nx, ny))

        next_positions = set(new_positions)
        for n_pos in set(new_positions):
            if n_pos in set(even_steps) :
                next_positions.remove(n_pos)
            if n_pos in set(odd_steps) :
                next_positions.remove(n_pos)

        positions = next_positions

    return even_steps, odd_steps

def mark_on_map(garden, positions, symbol) :
    for x, y in positions :
        garden[y][x] = symbol
    return garden

def print_map(garden) :
    for row in garden :
        print(''.join([c for c in row]))

def main():
    garden = read_data("day21/input")

    start = find_token(garden, 'S')
    steps = 64

    even_steps, odd_steps = explore(garden, start, ['S', '.'], steps)

    garden = mark_on_map(garden, even_steps, 'o')
    garden = mark_on_map(garden, odd_steps, 'x')

    print_map(garden)

    if steps % 2 == 0 :
        total = len(even_steps)
    else :
        steps = len(odd_steps)

    print(f"Part 1 {total}")

if __name__ == '__main__' :
    main()
