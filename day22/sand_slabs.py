from functools import cmp_to_key

class Brick() :
    def __init__(self, shape, position) -> None:
        self.shape = shape
        x, y, _ = position

        # Describe the plane seen from above as positive ranges
        self.xy_shape = self._find_xy_shape(shape, position)

        # Update z and the top level (if dz < 0, z and dz switch place)
        z, self.top_z_level = self._find_top_z_level(shape, position)
        self.position = x, y, z


    def _find_xy_shape(self, shape, position) :
        x, y, _ = position
        dx, dy, _ = shape

        front = lambda x, dx : min(x, x + dx)
        back = lambda x, dx : max(x, x + dx)

        rx = range(front(x, dx), back(x, dx) + 1)
        ry = range(front(y, dy), back(y, dy) + 1)

        return (rx, ry)

    def _find_top_z_level(self, shape, position) :
        _, _, z = position
        _, _, dz = shape
        return min(z, z + dz), max(z, z + dz) + 1

    def isOnTop(self, otherBrick):
        x_range, y_range = self.xy_shape
        x_other, y_other = otherBrick.xy_shape

        xs_range, ys_range = set(x_range), set(y_range)

        return len(xs_range.intersection(x_other)) > 0 and len(ys_range.intersection(y_other)) > 0

    def move(self, dz) :
        x, y, z = self.position
        z += dz
        z, self.top_z_level = self._find_top_z_level(self.shape, (x, y, z))
        self.position = (x, y, z)

def sortZLevel(brick1 : Brick, brick2 : Brick) :
    return brick1.top_z_level - brick2.top_z_level

class World():

    def __init__(self, bricks : list[Brick]) -> None:
        self.bricks = sorted(bricks, key=cmp_to_key(sortZLevel))

    def ground(self):
        # Push first brick to ground (which is at z = 1)
        _, _, z = self.bricks[0].position
        self.bricks[0].move(1 - z)

        grounded_bricks = [self.bricks[0]]
        for brick in self.bricks[1:]:
            # Default to move all the way to the ground
            z = brick.position[2]
            dz = 1 - z
            for grounded_brick in grounded_bricks :
                # If the brick intersects on xy plane with brick below, update dz
                if brick.isOnTop(grounded_brick) :
                    grounded_brick.top_z_level - z
                    dz = max(dz, grounded_brick.top_z_level - z)
            brick.move(dz)
            grounded_bricks.append(brick)

    def nSupportingAbove(self, bottomBrick : Brick) :
        n = 0
        for brick in self.bricks :
            _, _, z = brick.position
            if bottomBrick.top_z_level == z :
                if brick.isOnTop(bottomBrick) :
                    n += 1
        return n

    def supportingBelow(self, topBrick : Brick) :
        bricksBelow = []
        _, _, z = topBrick.position
        for brick in self.bricks :
            if brick.top_z_level == z :
                if topBrick.isOnTop(brick) :
                    bricksBelow.append(brick)
        return bricksBelow

    def nCanBeDisintegrated(self) :
        disintegratable = []
        must_keep = []
        for i, brick in enumerate(self.bricks) :
            c = chr((0x41 + i % 24))
            # More than one is supporting this brick
            bricksBelow = self.supportingBelow(brick)
            if len(bricksBelow) >= 2 :
                disintegratable.extend(bricksBelow)
            elif len(bricksBelow) == 1 :
                must_keep.extend(bricksBelow)
            # This brick doesn't support any brick
            if self.nSupportingAbove(brick) == 0 :
                disintegratable.append(brick)

        disintegratable = set(disintegratable)
        return len(disintegratable.difference(must_keep))

    def print_xz(self) :
        max_x, max_z = 0, 0
        for brick in self.bricks:
            x, _, _ = brick.position
            dx, _, _ = brick.shape
            z = brick.top_z_level
            max_x = max(max_x, x + dx + 1)
            max_z = max(max_z, z)

        area = []
        for z in range(max_z) :
            area.append(['.' for _ in range(max_x)])

        for i, brick in enumerate(self.bricks) :
            x, _, z = brick.position
            dx, _, dz = brick.shape
            for sx in range(x, x + dx + 1) :
                area[z][sx] = chr((0x41 + i % 24))
            for sz in range(z, z + dz + 1) :
                area[sz][x] = chr((0x41 + i % 24))

        print("XZ plane:")
        for line in reversed(area):
            print(''.join([c for c in line]))

    def print_yz(self) :
        max_y, max_z = 0, 0
        for brick in self.bricks:
            _, y, _ = brick.position
            _, dy, _ = brick.shape
            z = brick.top_z_level
            max_y = max(max_y, y + dy + 1)
            max_z = max(max_z, z)

        area = []
        for z in range(max_z) :
            area.append(['.' for _ in range(max_y)])

        for i, brick in enumerate(self.bricks) :
            _, y, z = brick.position
            _, dy, dz = brick.shape
            for sy in range(y, y + dy + 1) :
                area[z][sy] = chr((0x41 + i % 24))
            for sz in range(z, z + dz + 1) :
                area[sz][y] = chr((0x41 + i % 24))

        print("YZ plane:")
        for line in reversed(area):
            print(''.join([c for c in line]))

def read_data(file):
    with open(file) as f :
        lines = f.readlines()

    shapes, positions = [], []
    for line in lines :
        position, end = line.split('~')

        splitter = lambda x : [int(c) for c in x.split(',')]
        x, y, z = splitter(position)
        positions.append((x, y, z))

        xe, ye, ze = splitter(end)
        dx, dy, dz = xe - x, ye - y, ze - z
        shapes.append((dx, dy, dz))

    return shapes, positions

def main() :
    shapes, positions = read_data('day22/input')

    bricks = [Brick(shape, position) for shape, position in zip(shapes, positions)]

    world = World(bricks)
    world.ground()
    world.print_xz()
    world.print_yz()
    print(f"Part 1: {world.nCanBeDisintegrated()}")


if __name__ == '__main__' :
    main()
