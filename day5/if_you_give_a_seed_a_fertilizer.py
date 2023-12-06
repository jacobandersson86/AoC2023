import re

def calculate_offset_reverse(input, destination, source, range):
    offset = source - destination
    if input >= destination and input < destination + range:
        return offset
    return 0

def find_input(expression, content):
    stop_expr = "\n\n"
    loc = content.find(expression)
    stop = content[loc:].find(stop_expr) + loc
    line = content[loc:stop]
    return [int(v) for v in re.findall("[0-9]+", line)]

def chunks(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]


def generate_seed_ranges(seeds):
    seed_pairs = chunks(seeds, 2)

    ranges = []
    for size, length in seed_pairs:
        ranges.append(range(size, size + length))
    return ranges

def main() :
    with open("day5/example") as f:
        content = f.read()

    seeds = find_input("seeds:", content)

    map_keywords = [
        "seed-to-soil map:",
        "soil-to-fertilizer map:",
        "water-to-light map:",
        "light-to-temperature map:",
        "temperature-to-humidity map",
        "humidity-to-location map:"
    ]

    maps = []
    for key in map_keywords:
        map = find_input(key, content)
        map = chunks(map, 3)
        maps.append(map)

    seed_ranges = generate_seed_ranges(seeds)

    location = 0
    found = False
    while not found:
        offset = 0
        seed = location
        for map in maps[::-1]:
            for destination, source, range in map:
                offset = calculate_offset_reverse(seed, destination, source, range)
                if (offset) :
                    seed += offset
                    break
        for seed_range in seed_ranges:
            if seed in seed_range:
                found = True
        if not found:
            location += 1

    print(f"Smallest location is {location}")

if __name__ == '__main__' :
    main()
