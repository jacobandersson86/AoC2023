import re

def read_data(file) :
    with open(file) as f:
        lines = f.readlines()

    sequences = []
    for line in lines:
        sequence = re.findall("[-0-9]+", line)
        sequence = [int(v) for v in sequence]
        sequences.append(sequence)

    return sequences

def extend(sequence) :
    diffs = []
    for i in range(len(sequence) - 1) :
        diffs.append(sequence[i + 1] - sequence[i])

    if not all(e == 0 for e in diffs) :
        new_sequence = extend(diffs)
        sequence.append(new_sequence[-1] + sequence[-1])

    return sequence

def prepend(sequence) :
    diffs = []
    for i in range(len(sequence) - 1) :
        diffs.append(sequence[i + 1] - sequence[i])

    if not all(e == 0 for e in diffs) :
        new_sequence = prepend(diffs)
        sequence.insert(0, sequence[0] - new_sequence[0])

    return sequence


def main():
    sequences = read_data("day9/input")

    for sequence in sequences:
        sequence = extend(sequence)
        print(sequence)

    total = sum([s[-1] for s in sequences])

    print(f"Part 1: {total}")

    for sequence in sequences[::-1]:
        sequence = prepend(sequence)
        print(sequence)

    total = sum([s[0] for s in sequences])
    print(f"Part 2: {total}")


if __name__ == '__main__' :
    main()
