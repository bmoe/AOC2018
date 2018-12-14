
UP = '^'
DOWN = 'v'
LEFT = '<'
RIGHT = '>'

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

data = '13-input'
test_data = '13-input-test'

# Moving onto this thing, going this direction.
# You are now going this possibly new direction.
# Intersections are crazy though.  Gotta ask the
# car for that one.
# So .. map road kind -> current dir -> next dir
next_direction = {
    '-': {RIGHT: RIGHT, LEFT: LEFT},
    '|': {DOWN: DOWN, UP: UP},
    '/': {UP: RIGHT, LEFT: DOWN, DOWN: LEFT, RIGHT: UP},
    '\\': {UP: LEFT, LEFT: UP, DOWN: RIGHT, RIGHT: DOWN},
}

turn_cycle = [
    {UP: LEFT, LEFT: DOWN, DOWN: RIGHT, RIGHT: UP},  # Left turn
    {UP: UP, LEFT: LEFT, DOWN: DOWN, RIGHT: RIGHT},  # Forward
    {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP},  # Right turn
]


def next_position(pos, direction):
    y, x = pos
    if direction == UP:
        return (y-1, x)
    if direction == DOWN:
        return (y+1, x)
    if direction == LEFT:
        return (y, x-1)
    if direction == RIGHT:
        return (y, x+1)


class Car:
    def __init__(self, position, on):
        self.position = position
        self.is_on = on  # road glyph we are on
        self.nturns = 0
        self.crashed = False  # Did some idiot hit us?

    def next_direction(self, current_direction):
        # Where we will go at an intersection
        next_direction = turn_cycle[self.nturns % 3][current_direction]
        self.nturns += 1
        return next_direction

    def __repr__(self):
        y, x = self.position
        return "Car<({},{}) turned: {}>".format(x, y, self.nturns)


class Track:
    def __init__(self, fname):
        # Grid coordinates are:
        #   y = row from top
        #   x = col from left
        cars = []
        grid = []
        for y, row in enumerate(open(fname, 'r').readlines()):
            row = list(row.rstrip('\n'))
            grid.append(row)
            for x, cell in enumerate(row):
                # Find the cars
                if cell in DIRECTIONS:
                    # Rashly assume we never start in
                    # an intersection nor a corner
                    # So the road tile we start on is | or -
                    cars.append(
                        Car(
                            (y, x),
                            {UP: '|', DOWN: '|', LEFT: '-', RIGHT: '-'}[cell]
                        )
                    )
        self.cars = cars
        self.grid = grid
        self.crashed = []
        self.time = 0

    def tick(self):
        sorted_cars = sorted(self.cars, key=lambda car: car.position)
        for car in sorted_cars:
            if car.crashed:
                # We are no longer in the game.  So sad.
                assert car in self.crashed
                assert car not in self.cars
                continue
            y, x = car.position
            # Find direction of this car
            d = self.grid[y][x]
            # Where will it be next?
            (nexty, nextx) = next_position((y, x), d)

            old_road = car.is_on
            self.grid[y][x] = old_road

            new_road = self.grid[nexty][nextx]
            car.is_on = new_road
            car.position = (nexty, nextx)

            # What is here and what will be here?
            if new_road in DIRECTIONS:
                # CRASH
                self.cars.remove(car)
                self.crashed.append(car)
                # Find our victim
                victim = [c for c in self.cars if c.position == car.position]
                assert len(victim) == 1
                victim = victim[0]
                victim.crashed = True
                self.cars.remove(victim)
                self.crashed.append(victim)
                what_will_be = victim.is_on
            elif new_road == '+':
                # Intersection
                what_will_be = car.next_direction(d)
            else:
                # Boring
                what_will_be = next_direction[new_road][d]
            self.grid[nexty][nextx] = what_will_be

    def __repr__(self):
        the_map = '\n'.join([''.join(row) for row in self.grid])
        return "{}\nTime: {}\nCars:\n{}\nCrashed:\n{}".format(
            the_map, self.time, self.cars, self.crashed)


def first_test():
    t = Track(test_data)
    while not t.crashed:
        print(t)
        t.tick()
    print(t)


def first():
    t = Track(data)
    while not t.crashed:
        print(t)
        t.tick()
    print(t)


def second():
    t = Track(data)
    while len(t.cars) > 1:
        print(t)
        t.tick()
    print(t)
