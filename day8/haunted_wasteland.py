import re
import math

direction = {
    "L" : 0,
    "R" : 1
}

def read_input(file):
    with open(file) as f:
        lines = f.readlines()

    sequence = lines[0].strip("\n")

    mmap = {}
    for line in lines[2:]:
        start, left, right = re.findall("([A-Z0-9]+)", line)
        mmap[start] = (left, right)

    return sequence, mmap

def spawn(mmap):
    keys = mmap.keys()
    return [key for key in keys if key[2] == "A"]

'''
A repeat is when we find the same zed at the same step in the sequence
This means that the pattern must repeat.
'''
def find_repeat(mmap, sequence, spawn) :
    n_steps  = 0
    next_pos = spawn
    solved = False
    zeds = {}
    step_counts = []
    while not solved :
        for i, step in enumerate(sequence) :
            start_pos = next_pos
            next_pos = mmap[start_pos][direction[step]]
            n_steps += 1
            if next_pos[2] == "Z" :
                step_counts.append(n_steps)
                if next_pos in zeds :
                    if i in zeds[next_pos] :
                        solved = True
                        break
                    else :
                        zeds[next_pos].append(i)
                else :
                    zeds[next_pos] = [i]

    start  = step_counts[0]
    step_counts = [d - start for d in step_counts[1:]]

    return start, step_counts

def main():
    sequence, mmap = read_input("day8/input")

    # Part 1
    n_steps =0
    next_pos = "AAA"
    solved = False
    while not solved :
        for step in sequence:
            start_pos = next_pos
            next_pos = mmap[start_pos][direction[step]]
            n_steps += 1
            if next_pos == "ZZZ":
                print(f"Part 1. Found {next_pos} after {n_steps}")
                solved = True

    # Part 2

    spawns = spawn(mmap)
    print(spawns)

    distances = []
    for sp in spawns :
        start_distance, periods = find_repeat(mmap, sequence, sp)
        print(f"Spawn : '{sp}' Start : {start_distance} periods : {periods}")
        distances.append((start_distance, periods))

    periods = [period for _, period in distances]

    '''
    Brute force method. Didn't work, but kept as I found it interesting.
    '''
    # iterators = [0] * len(distances)
    # totals = [start for start, _ in distances]
    # while True :
    #     max_total = max(totals)
    #     for d, total in enumerate(totals):
    #         if total < max_total:
    #             totals[d] += periods[d][iterators[d] % len(periods[d])]
    #             iterators[d] += 1

    #     if max(totals) - min(totals) == 0:
    #         print(f"All on a 'z' after {totals[0]} steps")
    #         break

    '''
    Luckily all the starts where the same as the periods. An the periods of
    length 1. This means that we can take advantage of this and just find
    the least common denominator (lcm).
    '''
    periods = [item for period in periods for item in period]
    repeat_at = math.lcm(*periods)
    print(f"Part 2: Pattern repeats after {repeat_at} steps")

if __name__ == '__main__' :
    main()
