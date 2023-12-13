import re
import itertools

def read_file(file) :
    with open(file) as f :
        lines = f.readlines()

    records, groups = [], []
    for line in lines :
        record, group_string = line.strip('\n').split(' ')
        records.append(record)

        group = re.findall('[0-9]+', group_string)
        group = [int(v) for v in group]
        groups.append(group)

    return records, groups

def create_group_from_record(record) :
    springs = re.findall("[#]+", record)
    groups = [spring.count('#') for spring in springs]
    return groups

def create_possible_records(record, group) :
    replaceable = [i for i, chr in enumerate(record) if chr == "?"]

    n_unknown = record.count('#')
    n_springs = sum(group)

    n_unknown_springs = n_springs - n_unknown
    n_unknown_empty = len(replaceable) - n_unknown_springs

    # print(f"n_unknown_springs {n_unknown_springs} n_unknown_empty {n_unknown_empty}")

    combinations = itertools.combinations(replaceable, n_unknown_springs)

    possible_records = []
    for combo in combinations:
        possible = record
        for i in combo :
            possible = possible[:i] + '#' + possible[i + 1:]

        rest = list(set(replaceable) - set(combo))
        for r in rest :
            possible = possible[:r] + '.' + possible[r + 1:]

        possible_records.append(possible)

    return possible_records

def unfold(records, groups) :
    new_records, new_groups = [], []
    for record, group in zip(records, groups) :
        new_records.append("?".join([record]*5))
        new_groups.append(group * 5)

    return new_records, new_groups


def main():
    records, groups = read_file("day12/example")

    records, groups = unfold(records, groups)

    total = 0
    for record, group in zip(records, groups) :
        possible_records = create_possible_records(record, group)

        count = 0
        for record in possible_records:
            this_group = create_group_from_record(record)

            if this_group == group :
                count += 1

        # print (f"Found {count} combinations that fits in {record}, {group}")
        total += count

    print(f"Part 1: {total}")


if __name__ == '__main__' :
    main()
