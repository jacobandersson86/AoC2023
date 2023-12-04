def read_file(file) :
    with open(file) as f:
        lines = f.readlines()

    catalog = [line.strip("\n").replace(".", " ") for line in lines]
    return catalog

def find_symbol(catalog):
    symbols = []
    for y, line in enumerate(catalog):
        for x, char in enumerate(line):
            if not char.isnumeric() and char != " ":
                symbols.append((x, y))
    return symbols

def find_star(catalog):
    symbols = []
    for y, line in enumerate(catalog):
        for x, char in enumerate(line):
            if char == "*":
                symbols.append((x, y))
    return symbols

def get_grid(x, y, x_len = 1, y_len = 1):
    grid = []
    for xi in range(x - 1, x + x_len + 1):
        for yi in range(y - 1, y + y_len + 1):
            if yi == y :
                if xi >= x and xi < x + x_len :
                    continue
            grid.append((xi, yi))
    return grid

def keep_only_numbers(catalog) :
    new_catalog = []
    for line in catalog :
        new_line = ""
        for c in line :
            if not c.isnumeric():
                c = " "
            new_line = new_line + c
        new_catalog.append(new_line)

    return new_catalog

def find_numbers(catalog) :
    numbers = []
    catalog = keep_only_numbers(catalog)

    for y, line in enumerate(catalog):
        x = 0
        for word in line.split(" "):
            if word.isnumeric() :
                v = int(word)
                grid = get_grid(x, y, len(word))
                number = {"v" : v, "grid" : grid}
                numbers.append(number)
            x += len(word) + 1
    return numbers

def cull(numbers, acceptance):
    accepted = set(acceptance)
    accepted_numbers = []
    for number in numbers:
        hash = set(number["grid"])
        if set.intersection(hash, accepted) :
            accepted_numbers.append(number)
    return accepted_numbers

def find_gears(numbers, stars):
    gears = []
    for star in stars:
        star = set([star])
        possible_gears = []
        for number in numbers:
            grid = set(number["grid"])
            if set.intersection(grid, star) :
                possible_gears.append(number['v'])
        if len(possible_gears) == 2 :
            gears.append(possible_gears[0] * possible_gears[1])
    return gears

def main() :

    catalog = read_file("day3/input")

    #Part 1
    # Find all symbols
    symbols = find_symbol(catalog)

    # Find all numbers ( a number is digits that are in a sequence)
    # put them with a list of coordinate that forms a grid around them
    numbers = find_numbers(catalog)

    # Remove numbers that does not have symbols inside of the sorounding grid.
    numbers = cull(numbers, symbols)

    total = 0
    for number in numbers :
        total+= number['v']
    print(total)

    # Part 2
    # Find stars
    stars = find_star(catalog)

    # Reuse the numbers (that have a grid around them), find all occurrences with
    # exactly two numbers around a star
    gears = find_gears(numbers, stars)

    print(sum(gears))

if __name__ == '__main__' :
    main()
