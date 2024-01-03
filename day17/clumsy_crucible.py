import copy


class Crucible:
    all_visited_positions = []
    ds = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def __init__(self, start, goal, city_map) -> None:
        self.position = start
        self.goal = goal
        self.map = city_map
        x, y = start
        self.heat_loss = self.map[y][x]

        # Dictionary of my position and my value at this point
        self.my_visited_positions = {start : self.heat_loss}
        self.my_index = len(self.all_visited_positions)
        self.all_visited_positions.append(self.my_visited_positions)

        # Reset state keeping for straight lines
        self.last_position = start
        self.straight = 1
        self.steps = [start]

        # Activate
        self.active = True

    def __withinMap(self, position):
        x, y = position
        if x < 0 or y < 0 :
            return False
        if x >= len(self.map[0]) or y >= len(self.map) :
            return False
        return True

    def __take_step(self, position, forward_position):
        self.last_position = self.position
        if position == forward_position :
            self.straight += 1
        else :
            self.straight = 0

        self.steps.append(position)

        x, y = position
        self.heat_loss += self.map[y][x]

        self.position = position
        self.my_visited_positions[position] = self.heat_loss
        self.all_visited_positions[self.my_index][position] = self.heat_loss

        if position == self.goal :
            self.active = False

    def __add_spawn(self) :
        self.all_visited_positions.append(dict(self.my_visited_positions))
        self.my_index = len(self.all_visited_positions) - 1

    def roll(self) :
        if not self.active :
            return None

        x, y = self.position
        # Find the possible new positions
        possible_positions = set([(x + dx, y + dy) for dx, dy in self.ds])

        # Remove where we came from
        removable = set()
        removable.update([self.last_position])

        # Remove straight ahead if we've taken 3 steps in a row in same
        lx, ly = self.last_position
        dx, dy = x - lx, y - ly
        forward_position = (x + dx, y + dy)
        # if self.straight >= 3 :
        if len(self.steps) >= 3 :
            last_steps = self.steps[-4:]
            last_x, last_y = zip(*last_steps)
            if all([last_x[0] == i for i in last_x]) or all([last_y[0] == i for i in last_y]) :
                removable.update([forward_position])

        for pos in possible_positions :
            # Remove positions outside of map :
            if not self.__withinMap(pos) :
                removable.update([pos])

            # Remove steps I have visited :
            if pos in self.my_visited_positions :
                removable.update([pos])

            # Remove steps someone have visited and had less or equal than me
            for visited in self.all_visited_positions :
                # if any([pos in visited for pos in possible_positions]) :
                if pos in visited :
                    x, y = pos
                    if visited[pos] <= self.heat_loss + self.map[y][x] :
                        removable.update([pos])

        for pos in removable :
            if pos in possible_positions :
                possible_positions.remove(pos)

        if len(possible_positions) == 0 :
            self.active = False
            return None

        # Now all candidates are chosen, take a step in each direction

        # These will be my spawns
        spawns = []
        possible_positions = [pos for pos in possible_positions]
        for pos in possible_positions[1:] :
            spawn = copy.deepcopy(self)
            spawn.__add_spawn()
            spawn.__take_step(pos, forward_position)
            spawns.append(spawn)

        # The first is me
        self.__take_step(possible_positions[0], forward_position)

        return spawns

def read_file(file) :
    with open(file) as f:
        lines = f.readlines()

    city_map = []
    for line in lines :
        row = [int(c) for c in line.strip('\n')]
        city_map.append(row)
    return city_map

def any_active(crucibles) :
    return any(c.active for c in crucibles)

def print_map(mirror_map, crucibles : [Crucible]):
    visited = set()

    for crucible in crucibles :
        visited.update(crucible.my_visited_positions)

    mirror_map = copy.deepcopy(mirror_map)
    for position in visited :
        x, y = position
        mirror_map[y][x] = 'x'
    for row in mirror_map:
        line = ''.join([str(c) for c in row])
        print(line)

def least_active(crucibles) :
    heat_losses = [c.heat_loss for c in crucibles if c.active]
    active = [c for c in crucibles if c.active]
    least = min(heat_losses)
    return active[heat_losses.index(least)], least

def least_heat_loss(crucibles) :
    heat_losses = [c.heat_loss for c in crucibles if c.position == c.goal]
    finishers = [c for c in crucibles if c.position == c.goal]
    least = min(heat_losses)
    return finishers[heat_losses.index(least)], least


def main() :
    city_map = read_file("day17/example")

    crucible = Crucible((0, 0), (len(city_map[0]) - 1, len(city_map) - 1), city_map)
    crucibles = [crucible]
    while any_active(crucibles) :
    # for _ in range(200):
        if any_active(crucibles):
            shortest, heat_loss = least_active(crucibles)
        new_crucibles = []
        for crucible in crucibles:
        # crucible = shortest
            # print_map(city_map, [shortest])
            spawns = crucible.roll()
            if spawns is not None :
                new_crucibles.extend(spawns)

        crucibles.extend(new_crucibles)
        # print_map(city_map, crucibles)

        n_active = sum([1 for c in crucibles if c.active])
        print(f"Shortest {heat_loss} at position{shortest.position}")
        print(f"{n_active} / {len(crucibles)}")

    shortest, heat_loss = least_heat_loss(crucibles)
    print(shortest.steps)
    print_map(city_map, [shortest])

    print(f"Part 1 : {heat_loss}")



if __name__ == '__main__' :
    main()

