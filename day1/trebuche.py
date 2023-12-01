numbers = {
    "zero"  : 0,
    "one"   : 1,
    "two"   : 2,
    "three" : 3,
    "four"  : 4,
    "five"  : 5,
    "six"   : 6,
    "seven" : 7,
    "eight" : 8,
    "nine"  : 9
}

def main() :
    with open("./day1/input") as f:
        lines = f.readlines()

    found_numbers = []
    for line in lines:
        n = []
        for i, c in enumerate(line):
            if c.isnumeric() :
                n.append(int(c))
                continue

            stripped = line[i:]
            for key in numbers.keys():
                first_word = stripped[:len(key)]
                if key in first_word:
                    n.append(numbers[key])
                    continue

        v = n[0] * 10 + n[-1]
        found_numbers.append(v)

    print(sum(found_numbers))

if __name__ == '__main__' :
    main()
