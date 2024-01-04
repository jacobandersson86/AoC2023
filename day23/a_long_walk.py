
class Path() :
    ds = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    forbidden = {
        (-1,  0) : '<',
        ( 1,  0) : '>',
        ( 0, -1) : '^',
        ( 0,  1) : 'v',
    }

    def __init__(self, startingPoint, firstStep, distance, forrestMap) -> None:
        self.startingPoint = startingPoint
        self.firstStep = firstStep
        self.visited = [startingPoint, firstStep]
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
        next_steps = list(set(next_steps).difference([self.visited[-2]]))

        # Check if we are at a fork (which means we have more than one opportunity)
        if len(next_steps) > 1 :
            return True, (self.visited[-1])

        # Check that we do not go uphill
        for x, y in next_steps:
            if self._isUphill((x, y), self.visited[-1]) :
                return False, (x, y)

        # We might be at the goal (or dead end)
        if len(next_steps) == 0 :
            return True, (self.visited[-1])

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

    def __init__(self, position, distance, enteringPath, forrestMap) -> None:
        self.position = position
        self.distance = distance
        self.enteringPath = enteringPath

        self.attachingPaths = []
        if enteringPath :
            self.attachingPaths.append(enteringPath)

        self.forrestMap = forrestMap


    def findPaths(self) -> list[Path] :
        possible_steps = set(self.tryStep())

        # Remove steps that we came from
        for path in self.attachingPaths :
            possible_steps = possible_steps.difference(path.visited)

        # Return a new path for each direction due to be explored
        new_paths = []
        for step in possible_steps :
            new_paths.append(Path(self.position, step, self.distance, self.forrestMap))

        self.attachingPaths.extend(new_paths)
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
        self.attachingPaths.append(path)

        # If the new distance is greater, wipe attaching paths, and rediscover
        if path.distance > self.distance :
            self.attachingPaths = [path]
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

def update_distances(forks : list[Trailfork]):
    added = 1
    while added :
        added = 0
        for fork in forks :
            added += fork.updateDistance()

def main() :
    forrest_map = read_data('day23/example')

    '''
    Part 1
    Basically apply Dijkstra but instead of finding the shortest path, find the longest.
    Discard and found paths going uphill.
    0. Explore all paths from the Trailfork with the HIGHEST score.
    1. From the Trailfork, find all possible Paths.
    2. Explore each path until the it reaches a Trailfork or the goal.
        a. If the fork is unvisited, set the present score
        b. If the fork has never been seen, set the highest score.
        c. If a paths goes uphill, don't update the fork.
    4. (Not Dijkstra), continue to explore until no more unchartered paths can be found.
    5. If at the goal, do not explore new paths, (instead we try to reach this point)

    When all paths have been explored, the "goal" trailfork should contain the longest path.
    '''

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
            fork = fork_at_position(fork_position, forks)
            if fork is not None :
                pathQueue.extend(fork.updateDistance(path))
            else :
                forks.append(Trailfork(fork_position, path.distance, path, forrest_map))
                pathQueue.extend(forks[-1].findPaths())

    goalPosition = (len(forrest_map[0]) - 2, len(forrest_map) - 1)

    endFork = fork_at_position(goalPosition, forks)
    print(f"Part 1: {endFork.distance}")


if __name__ == '__main__' :
    main()
