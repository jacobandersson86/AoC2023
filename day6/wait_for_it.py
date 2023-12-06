import math

example = [
    [71530],
    [940200]
]

input = [
    [59796575], # Time
    [597123410321328] #  (Record) Distance
]

def solve(time, distance):
    s1 = time/2 + math.sqrt((time/2)**2 - distance)
    s2 = time/2 - math.sqrt((time/2)**2 - distance)

    if s2 < s1 :
        s = s1
        s1 = s2
        s2 = s

    # Convert to int, but we only accept the range where we travel longer than distance
    s1_int = math.ceil(s1)
    if s1_int == s1 :
        s1_int += 1
    s2_int = math.floor(s2)
    if s2_int == s2 :
        s2_int -= 1

    return (s1_int, s2_int)

def main():
    # This is just math!
    # distance = speed * time
    # speed = t_p
    # time = t - t_p
    # -> d = t*t_p - t^2

    # Find all t where d > record
    data = input
    table = zip(data[0], data[1])
    solutions = []
    for time, distance in table:
        solutions.append(solve(time, distance))

    total = 1
    for s1, s2 in solutions:
        r = s2-s1+1
        total *= r

    print(total)

if __name__ == '__main__' :
    main()
