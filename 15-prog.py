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

    def __repr__(self):
        return '{}({})'.format(self.glyph, self.health)

    def __str__(self):
        return self.glyph

    def __isub__(self, aggressor):
        # Gratuitous goofiness.
        # I will probably regret this.
        self.health -= aggressor.attack_power
        return self


class Elf(Guy):
    glyph = 'E'
    enemy = 'G'


class Goblin(Guy):
    glyph = 'G'
    enemy = 'E'


the_map = None
round = 0
elves = {}
goblins = {}
max_x = 0
max_y = 0


def load_data(data):
    global the_map, max_x, max_y
    the_map = []

    if hasattr(data, 'readlines'):
        lines = data.readlines()
    else:
        lines = data.strip().split('\n')

    for y, row in enumerate(lines):
        the_map.append(row)
        for x, sq in enumerate([ch for ch in row]):
            if sq == 'E':
                elves[(x, y)] = Elf()
            if sq == 'G':
                goblins[(x, y)] = Goblin()

    max_x = len(the_map[0]) - 1
    max_y = len(the_map) - 1


def load_file(fname):
    load_data(open(fname, 'r').read())


def _show_row(y, row, all_guys):
    guys = []
    for x, guy in enumerate(row):
        if guy in [GOBLIN, ELF]:
            try:
                assert (x, y) in all_guys
            except AssertionError:
                print('x,y guy :{},{}  {}\n{}'.format(x, y, guy, all_guys))
                print(the_map)
                raise
            guys.append(repr(all_guys[(x, y)]))
    return ''.join(row) + '  ' + ', '.join(guys)


def showstr():
    all_guys = dict(elves)
    all_guys.update(goblins)
    print('ALL GUYS IN: {}'.format(all_guys))
    return '\n'.join(
        _show_row(y, row, all_guys)
        for y, row in enumerate(the_map))


def show(overlay=None, overlay_ch='!'):
    all_guys = dict(elves)
    all_guys.update(goblins)
    if overlay:
        overlay = {k: overlay_ch for k in overlay}
    else:
        overlay = overlay or {}

    for y, row in enumerate(the_map):
        our_guys = []
        for x, sq in enumerate(row):
            sys.stdout.write(overlay.get((x, y), sq))
            # remember scores for this row
            if (x, y) in all_guys:
                our_guys.append(all_guys[(x, y)])
        if our_guys:
            sys.stdout.write('  ')
        sys.stdout.write(', '.join(map(repr, our_guys)))
        sys.stdout.write('\n')
    sys.stdout.flush()


def open_neighbors(x, y, match=FLOOR):
    # Given a position, what adjacent positions
    # match what we are looking for?
    possible = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
    return [
        (x, y) for (x, y) in possible
        if (
                x >= 0 and y >= 0 and
                x <= max_x and y <= max_y and
                the_map[y][x] == match
        )
    ]


def can_attack(x, y, enemy):
    return open_neighbors(x, y, enemy)


def paths_next(live, shortests):
    # calculate paths_n+1 by extending live paths by on step
    # live :: list of live paths
    # shortests :: dict(pos -> path) shortest path to pos
    still_alive = []
    for path in live:
        this_spot = path[0]
        next_spots = open_neighbors(*this_spot)
        for pos in next_spots:
            if pos not in shortests:
                newpath = [pos] + path
                still_alive.append(newpath)
                shortests[pos] = newpath
    return still_alive, shortests


def paths_zero(guy):
    live = [[guy]]  # one path of length one.
    shortests = {}
    return live, shortests


def target_spots(guys):
    "Get a bunch of coordinates, return a bunch of nearby squares"
    targets = []
    for guy in guys:
        targets.extend(open_neighbors(*guy))
    return targets


def next_step(guy, targets):
    acc, pathdir = paths_zero(guy)
    candidates = []
    while acc:
        # Check if a target has a path
        for t in targets:
            # We found a path.  Let's remember the first step on this path.
            if t in pathdir:
                # Last value because we store our path in reverse
                candidates.append(pathdir[t][-1])
        if candidates:
            break
        acc, pathdir = paths_next(acc, pathdir)

    return sorted(candidates, key=lambda pos: (pos[1], pos[0]))


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


def step():
    all_guys = dict(elves)
    all_guys.update(goblins)

    enemies_of = {
        'E': goblins,
        'G': elves,
    }

    order_of_play = sorted(all_guys.keys())
    print('ORDER: {}'.format(order_of_play))

    for guy_pos in order_of_play:
        guy = all_guys[guy_pos]
        victims = can_attack(*guy_pos, guy.enemy)
        if victims:
            victim_pos = sorted(victims)[0]
            print("{} IS HITTING {}".format(guy_pos, victim_pos))
            all_guys[x]
        else:
            targets = target_spots(enemies_of[guy.glyph].keys())
            print('Tryna find step {} to {}'.format(guy_pos, targets))
            steps = next_step(guy_pos, targets)  # oh lordy
            print('got: {}'.format(steps))
            if steps:
                print("GUY {} WANTS TO GO TO {}".format(guy_pos, steps[0]))
            else:
                # I think this means we are done?
                print("GUY {} HAS NO STEPS".format(guy_pos))
                assert not targets, 'Is {} not empty?'.format(targets)


if __name__ == "__main__":
    # load_file('15-input-test')
    load_data(goober2)
