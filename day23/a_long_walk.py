import copy
class Path() :
    ds = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    forbidden = {
        (-1,  0) : '<',
        ( 1,  0) : '>',
        ( 0, -1) : '^',
        ( 0,  1) : 'v',
    }

    def __init__(self, startingPoint, firstStep, distance, forrestMap, longestVisited = []) -> None:
        self.startingPoint = startingPoint
        self.firstStep = firstStep

        self.visited = []
        self.visited.extend(longestVisited[:])
        self.visited.extend([startingPoint, firstStep])

        self.forrestMap = forrestMap
        self.distance = distance + 1

    def _isUphill(self, next, last) :
        x, y = next
        lx, ly = last
        dx, dy = lx - x, ly - y
        forbidden = self.forbidden[(dx, dy)]

        if self.forrestMap[y][x] == forbidden :
            return True
        else :
            return False

    def _tryStep(self):
        # Try to take a step in each direction
        possible_steps = []
        for dx, dy in self.ds :
            # Start from the last position
            x, y = self.visited[-1]
            x, y = x + dx, y + dy

            # Don't try steps outside the map
            if x < 0 or x >= len(self.forrestMap[0]) :
                continue
            if y < 0 or y >= len(self.forrestMap) :
                continue

            if self.forrestMap[y][x] != '#':
                possible_steps.append((x, y))
        return possible_steps


    def _takeStep(self) :
        next_steps = self._tryStep()

        # Remove where we came from
        next_steps = list(set(next_steps).difference(self.visited))

        # Check if we are at a fork (which means we have more than one opportunity)
        if len(next_steps) > 1 :
            return True, (self.visited[-1])

        # Check that we do not go uphill
        for x, y in next_steps:
            if self._isUphill((x, y), self.visited[-1]) :
                return False, (x, y)

        # We might be at the goal (or dead end)
        if len(next_steps) == 0 :
            if self.visited[-1] == (len(self.forrestMap[0]) - 2, len(self.forrestMap) - 1) :
                return True, (self.visited[-1])
            return False, (self.visited[-1])

        # Okay, only one way to go, take the step.
        self.visited.append(next_steps[0])
        self.distance += 1
        return None, (next_steps[0])

    def explore(self) :
        found = None
        while found is None :
            found, next = self._takeStep()

        if found :
            return next
        else :
            return None


class Trailfork() :
    ds = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def __init__(self, position, distance, enteringPath : Path, forrestMap) -> None:
        self.position = position
        self.distance = distance

        self.enteringPaths = []
        self.longestVisited = []
        if enteringPath :
            self.enteringPaths.append(enteringPath)
            self.longestVisited = enteringPath.visited


        self.forrestMap = forrestMap


    def findPaths(self) -> list[Path] :
        possible_steps = set(self.tryStep())

        # Remove steps that we came from
        for path in self.enteringPaths :
            possible_steps = possible_steps.difference(path.visited)

        # Remove paths that means that we step on a visited place
        possible_steps = possible_steps.difference(self.longestVisited)

        # Return a new path for each direction due to be explored
        new_paths = []
        for step in possible_steps :
            new_paths.append(Path(self.position, step, self.distance, self.forrestMap, self.longestVisited))

        return new_paths


    def tryStep(self):
        # Try to take a step in each direction
        possible_steps = []
        for dx, dy in self.ds :
            x, y = self.position
            x, y = x + dx, y + dy

            # Don't try steps outside the map
            if x < 0 or x >= len(self.forrestMap[0]) :
                continue
            if y < 0 or y >= len(self.forrestMap) :
                continue

            if self.forrestMap[y][x] != '#':
                possible_steps.append((x, y))
        return possible_steps


    def updateDistance(self, path : Path) :
        self.enteringPaths.append(path)

        # If the new distance is greater, wipe attaching paths, and rediscover
        if path.distance >= self.distance :
            self.enteringPaths = [path]
            self.longestVisited = path.visited
            self.distance = path.distance
            return self.findPaths()

        return []


def read_data(file) :
    with open(file) as f:
        lines = f.readlines()

    forrest_map = []
    for line in lines :
        row = [c for c in line.strip('\n')]
        forrest_map.append(row)
    return forrest_map


def fork_at_position(position, forks : list[Trailfork]) -> Trailfork:
    for fork in forks :
        if fork.position == position :
            return fork
    return None


def print_longest_path(visited, forrest_map, token) :
    this_map = copy.deepcopy(forrest_map)
    for x, y in visited :
        this_map[y][x] = token
    return this_map


def print_map(this_map) :
    for line in this_map :
        print(''.join([c for c in line]))


def find_duplicates(data : list) :
    seen = set()
    dupes = []
    for x in data :
        if x in seen:
            dupes.append(x)
        else:
            seen.add(x)
    return dupes

def solve (forrest_map) :
    startPosition = (1, 0)
    startFork = Trailfork(startPosition, 0, None, forrest_map)
    forks = [startFork]
    newForks = [startFork]
    while len(newForks) != 0 :
        fork = newForks.pop(0)
        pathQueue = fork.findPaths()
        while len(pathQueue) != 0 :
            path = pathQueue.pop(0)
            fork_position = path.explore()

            # Dead end for this path, carry on and keep calm.
            if fork_position is None :
                continue

            # Update distances
            new_fork = fork_at_position(fork_position, forks)
            if new_fork is not None :
                lst = new_fork.updateDistance(path)
                if len(lst) > 0 :
                    newForks.append(new_fork)
            else :

                forks.append(Trailfork(fork_position, path.distance, path, forrest_map))
                newForks.append(forks[-1])

        longest = forks[0]
        for fork in forks :
            if fork.distance > longest.distance :
                longest = fork
        # new_map = print_longest_path(longest.longestVisited, forrest_map, 'o')
        # new_map = print_longest_path([longest.position], new_map, '+')
        # print_map(new_map)
        # print(f"Distance: {longest.distance}")

    goalPosition = (len(forrest_map[0]) - 2, len(forrest_map) - 1)
    endFork = fork_at_position(goalPosition, forks)

    new_map = print_longest_path(endFork.longestVisited, forrest_map, 'o')
    print('')
    fork_points = [fork.position for fork in forks]
    new_map = print_longest_path(fork_points, new_map, '+')
    print_map(new_map)

    print(f"Length: {len(set(endFork.longestVisited)) - 1}")

    dupes = find_duplicates(endFork.longestVisited)
    print(f"Duplicates {dupes}")

    return endFork.distance


def main() :
    forrest_map = read_data('day23/input')

    result = solve(forrest_map)
    print(f"Part 1: {result}")

    to_be_removed = set(['<', '>', 'v', '^'])
    for y, line in enumerate(forrest_map) :
        for x, c in enumerate(line) :
            if c in to_be_removed :
                forrest_map[y][x] = '.'

    result = solve(forrest_map)
    print(f"Part 2: {result}")

if __name__ == '__main__' :
    main()

# 7706 is to high
# 7698 is to high
