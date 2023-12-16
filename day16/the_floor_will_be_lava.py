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

    def __init__(self, position, direction, map) -> None:
        self.direction = direction
        self.position = position
        self.visited.update([(position, direction)])
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
                spawn = copy.deepcopy(self)
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
        return self.visited

def read_file(file) :
    with open(file) as f:
        lines = f.readlines()

    mirror_map = []
    for line in lines :
        row = [c for c in line.strip('\n')]
        mirror_map.append(row)
    return mirror_map

def print_map(mirror_map, beams : [Beam]):
    visited = set()

    for beam in beams :
        visited.update(beam.energized())

    mirror_map = copy.deepcopy(mirror_map)
    for position, _ in visited :
        x, y = position
        if mirror_map[y][x] == '.' :
            mirror_map[y][x] = 'x'
    for row in mirror_map:
        line = ''.join([c for c in row])
        print(line)

def all_visited(beams) :
    visited = set()
    for beam in beams :
        energy = beam.energized()
        for position, _ in energy :
            visited.update([position])
    return visited

def print_status_bar(beams, last_n_beams, last_n_active,) :
        n_beams = len(beams)
        n_actve = sum([1 for beam in beams if beam.canMove()])
        print(f"Beams: {n_beams:6}  Active: {n_actve:6}/{n_beams:6} Beam_rate: {n_beams - last_n_beams:6} Active rate:{n_actve - last_n_active:6}", end='\r')
        return n_beams, n_actve

def main() :
    mirror_map = read_file("day16/input")
    print_map(mirror_map, [])
    print('')

    beam = Beam((-1, 0), 'R', mirror_map)
    beams = [beam]

    last_n_beams = 0
    last_n_active = 0
    active = True
    while active :
        last_n_beams, last_n_active = print_status_bar(beams, last_n_beams, last_n_active)

        new_beams = []
        for beam in beams :
            spawn = beam.move()
            if spawn is not None :
                new_beams.append(spawn)

        if all([beam.canMove() == False for beam in beams]) :
            active = False

        beams.extend(new_beams)

    last_n_beams, last_n_active = print_status_bar(beams, last_n_beams, last_n_active)

    print('')
    visited = all_visited(beams)
    print(len(visited))

    print_map(mirror_map, beams)
    print('')

    # Remove one, since we started outside the grid.
    print(len(visited) - 1)

if __name__ == '__main__' :
    main()
