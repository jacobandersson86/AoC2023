
def read_input(file) :
    with open(file) as f:
        lines = f.readlines()

    patches = []
    patch = []
    for line in lines :
        if line != '\n' :
            patch.append(line.strip('\n'))
        else :
            patches.append(patch[:])
            patch = []

    # Add last patch
    patches.append(patch[:])
    patch = []

    return patches

def transpose(patch):
    height = len(patch)
    transposed_patch = []
    for column in range(len(patch[0])):
        line = ''.join([patch[row][column] for row in range(height)])
        transposed_patch.append(line)

    return transposed_patch

def print_patch(patch):
    for line in patch:
        print(line)


def find_mirror_line(patch) :
    candidates = []
    depths = []
    for i, (this, next) in enumerate(zip(patch, patch[1:])) :
        diff =  string_compare(this, next, 1)
        if diff <= 1 :
            found, depth = search_outward(patch, i, 1)
            if found :
                candidates.append(i)
                depths.append(depth)

    if len(candidates) == 0 :
        return 0

    ret = candidates[depths.index(max(depths))] + 1
    if len(candidates) > 1 :
        print(f"Found {len(candidates)}")

        print(f"Out of {candidates} with depths {depths}")
        print(f"Returning {ret}")

    return ret

def string_compare(str1, str2, limit) :
    diff = 0
    for c1, c2 in zip(str1, str2) :
        if c1 != c2 :
            diff += 1
        if diff > limit :
            return limit

    return diff

def search_outward(patch, line, limit) :
    # height = len(patch) - 1
    # search_depth = min(abs(line - height), line)

    # for i in range(search_depth):
    #     top = patch[line - i]
    #     bottom = patch[line + 1 + i]

    #     if bottom != top :
    #         return False, search_depth

    # return True, search_depth
    height = len(patch)
    search_depth = 0
    diff = 0

    for i in range(0, height):
        search_depth += 1

        lower = line - i
        upper = line + i + 1

        if lower < 0 or upper >= height :
            break

        top = patch[lower]
        bottom = patch[upper]

        diff += string_compare(top, bottom, limit)

        if diff > 1 :
            return False, search_depth

    if diff == 1 :
        return True, search_depth

    return False, search_depth



def main() :
    patches = read_input("day13/example")

    totals = []
    for patch in patches :
        rows = 0
        columns = 0
        print("Before")
        print_patch(patch)
        rows = find_mirror_line(patch)

        patch = transpose(patch)
        print("After:")
        print_patch(patch)
        columns = find_mirror_line(patch)

        if columns != 0 :
            rows = 0

        totals.append(columns + rows * 100)

    print(totals)
    print(f"Part 1: {sum(totals)}")


    # 34882 is to low
    # 32482 must be to low too....


if __name__ == '__main__' :
    main()
