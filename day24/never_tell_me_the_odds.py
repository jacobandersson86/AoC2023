from itertools import combinations

# TEST_MIN = 7
# TEST_MAX = 27
TEST_MIN = 200000000000000
TEST_MAX = 400000000000000

def linear_intersection(eq1, eq2) :
    k1, m1 = eq1
    k2, m2 = eq2

    # Find the intersection (formula from https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection)
    x0 = (m2 - m1) / (k1 - k2)
    y0 = k1*(m2 - m1) / (k1 - k2) + m1

    return x0, y0

def does_intersect(eq1, eq2, ranges1, ranges2, test_range) :
    k1, m1 = eq1
    k2, m2 = eq2

    # Lines with same slope cannot intersect (unless on exact same)
    if k1 == k2 :
        if m1 != m2 :
            return False
        else :
            print("Warning! Two lines are same, you must handle this case")
            return True

    x0, y0 = linear_intersection(eq1, eq2)
    x0, y0 = int(x0), int(y0)

    # Check if x0 and y0 is in the range (test area)
    if x0 not in ranges1[0] or x0 not in ranges2[0] :
        return False
    if y0 not in ranges1[1] or y0 not in ranges2[1] :
        return False
    if x0 not in test_range or y0 not in test_range :
        return False

    return True

def find_equation(px, py, vx, vy) :
    k = vy / vx
    m = py - k * px

    return (k, m)

def find_range(p, v):
    # NB. This assumes that p < TEST_MAX and vice versa.
    if v > 0 :
        this_range = range(p, TEST_MAX + 1)
    elif v < 0 :
        this_range = range(TEST_MIN, p +1)
    else :
        this_range = range(p, p + 1)
    return this_range

def read_data(file) :
    with open(file) as f :
        lines = f.readlines()

    positions, velocities = [],[]
    for line in lines :
        pos, vel = line.strip('\n').split('@')
        splitter = lambda x : [int(n) for n in x.split(',')]
        positions.append(splitter(pos))
        velocities.append(splitter(vel))

    return positions, velocities

def main() :
    positions, velocities = read_data('day24/input')

    equations = []
    ranges = []
    for (px, py, _), (vx, vy, _) in zip(positions, velocities) :
        equations.append(find_equation(px, py, vx, vy))
        ranges.append((find_range(px, vx), find_range(py, vy)))

    count = 0
    for item1, item2 in combinations(zip(equations, ranges), 2):
        eq1, r1 = item1
        eq2, r2 = item2
        if does_intersect(eq1, eq2, r1, r2, range(TEST_MIN, TEST_MAX)) :
            count += 1

    print(f"Part 1: {count}")


if __name__ == '__main__' :
    main()

