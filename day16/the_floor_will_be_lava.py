import copy

class Beam:
    translations = {
    'U' : ( 0, -1), # Positive y becomes downwards
    'D' : ( 0,  1),
    'L' : (-1,  0),
    'R' : ( 1,  0),
    }

    # '\'
    backslash = {
        'R' : 'D',
        'L' : 'U',
        'U' : 'L',
        'D' : 'R'
    }

    # '/'
    forwardslash = {
        'R' : 'U',
        'L' : 'D',
        'U' : 'R',
        'D' : 'L'
}
    visited = set()
    exits = set()

    def __init__(self, position, direction, map) -> None:
        self.direction = direction
        self.position = position
        self.visited = set()
        self.exits = set()
        self.map = map
        self.active = True

    def __withinMap(self, position):
        x, y = position
        if x < 0 or y < 0 :
            return False
        if x >= len(self.map[0]) or y >= len(self.map) :
            return False
        return True

    def move(self) :
        if not self.active :
            return None

        # Take one step in the direction
        x, y = self.position
        dx, dy = self.translations[self.direction]
        x, y = x + dx, y + dy

        if not self.__withinMap((x, y)) :
            self.active = False
            self.exits.update([(x, y)])
            return None

        self.position = (x, y)

        # Take an action depending on map.
        spawn_direction = None
        action = self.map[y][x]
        match action :
            case '.':
                # Do nothing, empty space
                pass
            case '\\' :
                self.direction = self.backslash[self.direction]
            case '/' :
                self.direction = self.forwardslash[self.direction]
            case '-' :
                if self.direction == 'U' or self.direction == 'D' :
                    self.direction = 'L'
                    spawn_direction = 'R'
                # else : do nothing
            case '|' :
                if self.direction == 'L' or self.direction == 'R' :
                    self.direction = 'U'
                    spawn_direction = 'D'
                # else : do nothing

        # Update visited. If we are at same position and same direction, then we
        # are in a loop
        if (self.position, self.direction) in self.visited :
            self.active = False
        else :
            self.visited.update([(self.position, self.direction)])

        # Make a spawn
        spawn = None
        if spawn_direction :
            if (self.position, spawn_direction) not in self.visited :
                spawn = copy.copy(self)
                spawn.direction = spawn_direction
                spawn.visited.update([(spawn.position, spawn.direction)])

        # Return spawn)
        return spawn

    def getPositionDirection(self) :
        return self.position, self.direction

    def canMove(self):
        return self.active

    def deactivate(self):
        self.active = False

    def energized(self):
        positions = set()
        for position, _ in self.visited :
            positions.update([position])
        return len(positions)

    def getVisited(self) :
        return self.visited

    def getExits(self) :
        return self.exits

def read_file(file) :
    with open(file) as f:
        lines = f.readlines()

    mirror_map = []
    for line in lines :
        row = [c for c in line.strip('\n')]
        mirror_map.append(row)
    return mirror_map

def beam_from(position, direction, mirror_map) :

    beam = Beam(position, direction, mirror_map)
    beams = [beam]

    active = True
    while active :

        new_beams = []
        for beam in beams :
            spawn = beam.move()
            if spawn is not None :
                new_beams.append(spawn)

        if all([beam.canMove() == False for beam in beams]) :
            active = False

        beams.extend(new_beams)

    return beams[0].energized(), beams[0].getExits()

def main() :
    mirror_map = read_file("day16/input")

    # Always start from outside, if the first position contains a mirror.
    energy, _ = beam_from((-1, 0), 'R', mirror_map)
    print(f"Part 1: {energy}")

    starts =      dict([((-1, i) ,                'R') for i in range(1, len(mirror_map))])
    starts.update(dict([((len(mirror_map[0]), i), 'L') for i in range(len(mirror_map))]))
    starts.update(dict([((i, -1),                 'D') for i in range(len(mirror_map[0]))]))
    starts.update(dict([((i, len(mirror_map)),    'U') for i in range(len(mirror_map[0]))]))

    energies = [energy]
    while len(starts) :
        pos, dir = starts.popitem()
        energized, exits = beam_from(pos, dir, mirror_map)
        energies.append(energized)
        for pos in exits :
            if pos in starts :
                del starts[pos]

    print(f"Part 2: {max(energies)}")

if __name__ == '__main__' :
    main()
