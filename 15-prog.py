import sys

GOBLIN = 'G'
ELF = 'E'
ROCK = '#'
FLOOR = '.'

TILES = [GOBLIN, ELF, ROCK, FLOOR]


def gridkey(pos):
    return (pos[1], pos[0])


class Guy:
    attack_power = 3
    health = 200
    glyph = '-'
    enemy = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def pos(self):
        return (self.x, self.y)

    def is_dead(self):
        return self.health <= 0

    def is_enemy(self, other):
        """I guess we hate guys who aren't our class"""
        return (
            isinstance(other, Guy) and
            not isinstance(other, self.__class__)
        )

    def __repr__(self):
        return '{}({})@{}'.format(self.glyph, self.health, self.pos())

    def __str__(self):
        return self.glyph

    def __isub__(self, aggressor):
        # Gratuitous goofiness.
        # I will probably regret this.
        self.health -= aggressor.attack_power
        return self

    def __lt__(self, other):
        x1, y1 = self.pos()
        x2, y2 = other.pos()
        return (y1, x1) < (y2, x2)


class Elf(Guy):
    glyph = 'E'


class Goblin(Guy):
    glyph = 'G'


class Map:
    def __init__(self, grid, elves, goblins):
        self.time = 0
        self.grid = grid
        self.elves = elves
        self.goblins = goblins
        self.corpses = set()

        self.max_x = len(grid[0]) - 1
        self.max_y = len(grid) - 1

        self.all_guys = {guy.pos(): guy for guy in self.elves | self.goblins}

    def show(self, overlay=None, overlay_ch='!'):
        if overlay:
            overlay = {k: overlay_ch for k in overlay}
        else:
            overlay = overlay or {}
        for y, row in enumerate(self.grid):
            our_guys = []
            for x, sq in enumerate(row):
                here = self[x, y]
                sys.stdout.write(overlay.get((x, y), str(here)))
                # remember scores for this row
                if isinstance(here, Guy):
                    our_guys.append(here)
            if our_guys:
                sys.stdout.write('  ')
            sys.stdout.write(', '.join(map(repr, our_guys)))
            sys.stdout.write('\n')
        sys.stdout.write('Round: {}\n'.format(self.time))
        sys.stdout.flush()

    def open_neighbors(self, pos, match=lambda x: x == FLOOR):
        # Given a position, what adjacent positions
        # match what we are looking for?
        x, y = pos
        possible = [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
        return [
            (x, y) for (x, y) in possible
            if match(self[x, y])
        ]

    def victims(self, guy):
        return [
            self[pos] for pos in self.open_neighbors(guy.pos(), guy.is_enemy)
        ]

    def paths_next(self, live, shortests):
        # calculate paths_n+1 by extending live paths by on step
        # live :: list of live paths
        # shortests :: dict(pos -> path) shortest path to pos
        still_alive = []
        for path in sorted(live, key=lambda pos: (pos[0][1], pos[0][0])):
            this_spot = path[-1]
            next_spots = self.open_neighbors(this_spot)
            # We count on neighbors being in reading order
            # So the first path we find for a position is the
            # most interesting, reading-order-wise.
            for pos in next_spots:
                if pos not in shortests:
                    newpath = path + [pos]
                    still_alive.append(newpath)
                    shortests[pos] = newpath
        return still_alive, shortests

    def paths_zero(self, guy):
        live = [[guy]]  # one path of length one.
        shortests = {}
        return live, shortests

    def target_spots(self, guys):
        "Get a bunch of coordinates, return a bunch of nearby squares"
        targets = []
        for guy in guys:
            targets.extend(self.open_neighbors(guy.pos()))
        targets.sort(key=gridkey)
        return targets

    def path_candidates(self, guy):
        # argh. why here?
        if self.victims(guy):
            # We can fight so we won't move
            return []

        acc, pathdir = self.paths_zero(guy.pos())
        if guy in self.elves:
            target_guys = self.goblins
        else:
            assert guy in self.goblins
            target_guys = self.elves
        target_spots = self.target_spots(target_guys)
        candidates = []
        while acc:
            # Check if a target has a path
            for t in target_spots:
                # We found a path.  Let's remember the first step on this path.
                if t in pathdir:
                    # This is our guy (target, first-step-on-path)
                    candidates.append((t, pathdir[t][1]))
            if candidates:
                # print('GOT CANDIDATES {}'.format(candidates))
                break
            acc, pathdir = self.paths_next(acc, pathdir)

        # Sort by target
        return sorted(candidates, key=lambda pos: (pos[0][1], pos[0][0]))

    def the_war_is_on(self):
        return self.elves and self.goblins

    def tick(self):
        order_of_play = sorted(list(self.elves | self.goblins))
        # print('ORDER: {}'.format(order_of_play))

        # I think this is wrong.  I think it is MOVE then FIGHT.
        for guy in order_of_play:
            if guy.is_dead():
                # print('oops, messing with a corpse at {}'.format(guy))
                continue

            # Move Stage
            steps = self.path_candidates(guy)
            if steps:
                # print("GUY {} WANTS TO GO TO {}".format(
                #     repr(guy), steps[0])
                # )
                next_x, next_y = steps[0][1]
                del self.all_guys[guy.pos()]
                guy.x = next_x
                guy.y = next_y
                self.all_guys[guy.pos()] = guy
            else:
                # print("GUY {} HAS NO STEPS".format(repr(guy)))
                pass

            # Fight Stage
            victims = self.victims(guy)
            if victims:
                # print("{} COULD hit {}".format(repr(guy), repr(victims)))
                # Pick on the weakest link you can reach
                victim = sorted(victims, key=lambda g: g.health)[0]
                # print("{} IS hitting {}".format(repr(guy), repr(victim)))
                victim -= guy  # pew pew pew
                if victim.is_dead():
                    # Oof. Remove the corpse.
                    # print('Dude {} he ded'.format(repr(victim)))
                    if victim in self.elves:
                        self.elves.remove(victim)
                    else:
                        self.goblins.remove(victim)
                    self.corpses.add(victim)
                    del self.all_guys[victim.pos()]

        self.time += 1
        # self.all_guys = {guy.pos(): guy for guy in self.elves | self.goblins}

    def run(self):
        self.show()
        print(80 * '=')
        while self.the_war_is_on():
            self.tick()
        self.show()
        print('Genocide complete at time {}'.format(self.time))
        print('Answer: {}'.format(
            self.time * sum([guy.health for guy in self.elves | self.goblins]))
        )

    def __getitem__(self, i):
        (x, y) = i
        try:
            return self.all_guys.get((x, y), self.grid[y][x])
        except IndexError:
            return None

    @classmethod
    def load(cls, data):
        if hasattr(data, 'readlines'):
            lines = data.readlines()
        else:
            lines = data.strip().split('\n')

        grid = []
        elves = set()
        goblins = set()

        for y, row in enumerate(lines):
            row = row.strip()
            grid_row = []
            for x, sq in enumerate([ch for ch in row]):
                if sq == 'E':
                    grid_row.append(FLOOR)
                    elves.add(Elf(x, y))
                elif sq == 'G':
                    grid_row.append(FLOOR)
                    goblins.add(Goblin(x, y))
                else:
                    grid_row.append(sq)
            grid.append(grid_row)

        return cls(grid, elves, goblins)


# Super baby movement test
test1 = """
#######
#.E...#
#.....#
#...G.#
#######
"""

# Simple movement and fighting
test2 = """
#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########
"""

# More obstacles
# Answer is 27730
#   200+131+59+200 = 590
#   47 * 590 = 27730
#
#  After 47 rounds:
#  #######
#  #G....#   G(200)
#  #.G...#   G(131)
#  #.#.#G#   G(59)
#  #...#.#
#  #....G#   G(200)
#  #######
#
test3 = """
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
"""


def first():
    # This got 199800.  But that is too high somehow.  Shit.
    Map.load(open('15-input', 'r')).run()
