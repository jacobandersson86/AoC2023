import numpy as np

def read_data(file):
    with open(file) as f :
        lines = f.readlines()

    star_map = np.zeros(shape=(len(lines), len(lines[0].strip('\n'))))

    star_count = 1
    for y, line in enumerate(lines):
        for x, chr in enumerate(line.strip('\n')):
            if chr != '.' :
                star_map[y, x] = star_count
                star_count += 1

    return star_map

def expand(star_map):
    ny, nx = star_map.shape
    insert_x = []
    for x in range(nx):
        if (star_map[:, x] == 0).all() :
            insert_x.append(x)

    insert_y = []
    for y in range(ny):
        if (star_map[y,:] == 0).all() :
            insert_y.append(y)

    for x in insert_x:
        star_map[:, x] = np.full(ny, -1)

    ny, nx = star_map.shape

    for y in insert_y:
        star_map[y, :] = np.full((1,nx), -1)

    return star_map

def find_stars(star_map):
    stars = np.argwhere(star_map > 0)
    return stars

def calc_distance(star_map, posA, posB, mul):
    ax, ay = posA
    bx, by = posB

    dx = bx - ax
    dy = by - ay

    count = 0

    sign_x = 1
    if dx < 0 :
        sign_x = -1

    sign_y = 1
    if dy < 0 :
        sign_y = -1

    for x in range(ax, bx + np.sign(dx), sign_x):
        if star_map[ay, x] == -1 :
            count += 1

    for y in range(ay, by + np.sign(dy), sign_y) :
        if star_map[y, bx] == -1 :
            count += 1

    return abs(dx) + abs(dy) + count * mul - count

def main():
    star_map = read_data("day11/input")

    star_map = expand(star_map)
    stars = find_stars(star_map)

    mul = 1000000
    distances = []
    for i in range(len(stars - 1)):
        for j in range(len(stars[1 + i:])) :
            ay, ax = stars[i]
            by, bx = stars[j+ i + 1]
            distance = calc_distance(star_map, (ax, ay),(bx, by), mul)
            distances.append(distance)

    print(sum(distances))

if __name__ == '__main__' :
    main()
