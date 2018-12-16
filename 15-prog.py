import sys

GOBLIN = 'G'
ELF = 'E'
ROCK = '#'
FLOOR = '.'

TILES = [GOBLIN, ELF, ROCK, FLOOR]


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
        return self.pos() < other.pos()


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
        sys.stdout.write('Round: {}'.format(self.time))
        sys.stdout.flush()

    def open_neighbors(self, pos, match=lambda x: x == FLOOR):
        # Given a position, what adjacent positions
        # match what we are looking for?
        x, y = pos
        possible = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
        return [
            (x, y) for (x, y) in possible
            if match(self[x, y])
        ]

    def victims(self, guy):
        return self.open_neighbors(guy.pos(), guy.is_enemy)

    def paths_next(self, live, shortests):
        # calculate paths_n+1 by extending live paths by on step
        # live :: list of live paths
        # shortests :: dict(pos -> path) shortest path to pos
        still_alive = []
        for path in live:
            this_spot = path[0]
            next_spots = self.open_neighbors(this_spot)
            for pos in next_spots:
                if pos not in shortests:
                    newpath = [pos] + path
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
        return targets

    def next_step(self, guy):
        acc, pathdir = self.paths_zero(guy.pos())
        if guy in self.elves:
            targets = self.goblins
        else:
            assert guy in self.goblins
            targets = self.elves
        targets = self.target_spots(targets)
        candidates = []
        while acc:
            # Check if a target has a path
            for t in targets:
                # We found a path.  Let's remember the first step on this path.
                if t in pathdir:
                    # Last value because we store our path in reverse
                    # Well, 2nd last because our guy's at the start of the path
                    candidates.append(pathdir[t][-2])
            if candidates:
                break
            acc, pathdir = self.paths_next(acc, pathdir)

        return sorted(candidates, key=lambda pos: (pos[1], pos[0]))

    def its_genocide(self):
        return not self.elves or not self.goblins

    def tick(self):
        order_of_play = sorted(list(self.elves | self.goblins))
        print('ORDER: {}'.format(order_of_play))

        for guy in order_of_play:
            if guy.is_dead():
                print('oops, messing with a corpse at {}'.format(guy))
                continue
            victim_positions = self.victims(guy)
            if victim_positions:
                victim = self[sorted(victim_positions)[0]]
                print("{} IS HITTING {}".format(guy, repr(victim)))
                victim -= guy  # pew pew pew
                if victim.is_dead():
                    # Oof. Remove the corpse.
                    print('Dude {} he ded'.format(repr(victim)))
                    if victim in self.elves:
                        self.elves.remove(victim)
                    else:
                        self.goblins.remove(victim)
                    self.corpses.add(victim)
                    del self.all_guys[victim.pos()]
            else:
                steps = self.next_step(guy)
                print('got: {}'.format(steps))
                if steps:
                    print("GUY {} WANTS TO GO TO {}".format(
                        repr(guy), steps[0])
                    )
                    next_x, next_y = steps[0]
                    del self.all_guys[guy.pos()]
                    guy.x = next_x
                    guy.y = next_y
                    self.all_guys[guy.pos()] = guy
                else:
                    # I think this means we are done?
                    print("GUY {} HAS NO STEPS".format(repr(guy)))
                    # Some group should have fallen to genocide
                    # Or maybe some sad group is surrounded and inaccessible
                    # assert not self.elves or not self.goblins

        self.time += 1
        # self.all_guys = {guy.pos(): guy for guy in self.elves | self.goblins}

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


# the_map = None
# theelves = set()
# thegoblins = set()
# max_x = 0
# max_y = 0


# def load_data(data):
#     global the_map, max_x, max_y
#     the_map = []

#     if hasattr(data, 'readlines'):
#         lines = data.readlines()
#     else:
#         lines = data.strip().split('\n')

#     for y, row in enumerate(lines):
#         the_map.append(row)
#         for x, sq in enumerate([ch for ch in row]):
#             if sq == 'E':
#                 theelves.add(Elf(x, y))
#             if sq == 'G':
#                 thegoblins.add(Goblin(x, y))

#     max_x = len(the_map[0]) - 1
#     max_y = len(the_map) - 1


# def load_file(fname):
#     load_data(open(fname, 'r').read())


# def _show_row(y, row, all_guys):
#     guys = []
#     for x, guy in enumerate(row):
#         if guy in [GOBLIN, ELF]:
#             try:
#                 assert (x, y) in all_guys
#             except AssertionError:
#                 print('x,y guy :{},{}  {}\n{}'.format(x, y, guy, all_guys))
#                 print(the_map)
#                 raise
#             guys.append(repr(all_guys[(x, y)]))
#     return ''.join(row) + '  ' + ', '.join(guys)


# def showstr():
#     all_guys = {elf.pos(): elf for elf in theelves}
#     all_guys.update({goblin.pos(): goblin for goblin in thegoblins})

#     print('ALL GUYS IN: {}'.format(all_guys))
#     return '\n'.join(
#         _show_row(y, row, all_guys)
#         for y, row in enumerate(the_map))


# def show(overlay=None, overlay_ch='!'):
#     all_guys = {elf.pos(): elf for elf in theelves}
#     all_guys.update({goblin.pos(): goblin for goblin in thegoblins})

#     if overlay:
#         overlay = {k: overlay_ch for k in overlay}
#     else:
#         overlay = overlay or {}

#     for y, row in enumerate(the_map):
#         our_guys = []
#         for x, sq in enumerate(row):
#             sys.stdout.write(overlay.get((x, y), sq))
#             # remember scores for this row
#             if (x, y) in all_guys:
#                 our_guys.append(all_guys[(x, y)])
#         if our_guys:
#             sys.stdout.write('  ')
#         sys.stdout.write(', '.join(map(repr, our_guys)))
#         sys.stdout.write('\n')
#     sys.stdout.flush()


goober = """
#######
#.E...#
#.....#
#...G.#
#######
"""

goober2 = """
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


goober3 = """
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
"""


# def badstep():
#     all_guys = dict(elves)
#     all_guys.update(goblins)

#     enemies_of = {
#         'E': goblins,
#         'G': elves,
#     }

#     order_of_play = sorted(all_guys.keys())
#     print('ORDER: {}'.format(order_of_play))

#     for guy_pos in order_of_play:
#         guy = all_guys[guy_pos]
#         victims = can_attack(*guy_pos, guy.enemy)
#         if victims:
#             victim_pos = sorted(victims)[0]
#             print("{} IS HITTING {}".format(guy_pos, victim_pos))
#             all_guys[x]
#         else:
#             targets = target_spots(enemies_of[guy.glyph].keys())
#             print('Tryna find step {} to {}'.format(guy_pos, targets))
#             steps = next_step(guy_pos, targets)  # oh lordy
#             print('got: {}'.format(steps))
#             if steps:
#                 print("GUY {} WANTS TO GO TO {}".format(guy_pos, steps[0]))
#             else:
#                 # I think this means we are done?
#                 print("GUY {} HAS NO STEPS".format(guy_pos))
#                 assert not targets, 'Is {} not empty?'.format(targets)


# if __name__ == "__main__":
#     # load_file('15-input-test')
#     load_data(goober2)
