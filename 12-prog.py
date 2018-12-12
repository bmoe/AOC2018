import functools

# initial state: ###....#..#..#......####.#..  ...
#
# XXXXX => X
#   ...

data = open('12-input', 'r').read()
test_data = open('12-input-test', 'r').read()


def parse(src):
    lines = src.split('\n')
    first_line = lines.pop(0)

    pots = first_line.split(':')[1].strip()
    rules = [(r[0:5], r[9]) for r in lines if r.strip() != '']

    return pots, rules


def dumb_prev_clusters(pots):
    """cluster[n] Five pots surrounding pot[n]"""

    def f(state, next_pot):
        (prev_cluster, clusters) = state
        this_cluster = prev_cluster[1:] + next_pot
        clusters.append(this_cluster)
        return (this_cluster, clusters)

    init_cluster = '...' + pots[0:2]

    _, clusters = functools.reduce(
        f, '.' + pots[1:] + '..', (init_cluster, []))
    return clusters


def prev_clusters(pots):
    # Thank you, Doctor Fritz!
    pots = '..' + pots + '.....'
    return map(''.join, zip(pots, pots[1:], pots[2:], pots[3:], pots[4:]))


class Garden:
    def __init__(self, pots, rules):
        self.rules = rules
        self.map_rules = dict(rules)
        self.pots = pots

        # Keep track of which pot is leftmost in our data
        # pots[n] == real_pots[n+offset]
        self.index_offset = 0
        self.generation = 0

        self.normalize()

    def pad(self):
        self.pots = '..' + self.pots
        self.index_offset -= 2

    def apply_rules(self, pot, cluster):
        for (pat, res) in self.rules:
            if cluster == pat:
                return res
        return '.'

    def next_gen(self):
        ng = []
        for (pot, cluster) in zip(self.pots + '..', prev_clusters(self.pots)):
            # next_guy = self.apply_rules(pot, cluster)
            next_guy = self.map_rules.get(cluster, '.')
            ng.append(next_guy)
        return ''.join(ng)

    def normalize(self):
        """Make sure we have two (and only two) empty pots at the left"""
        while self.pots[0] == '.':
            self.pots = self.pots[1:]
            self.index_offset += 1
        self.pad()
        self.pots = self.pots.rstrip('.')
        self.pots += ".."

    def answer(self):
        return sum(
            [i+self.index_offset
             for (i, p) in enumerate(self.pots) if p == '#']
        )

    def tick(self):
        self.pots = self.next_gen()
        self.generation += 1
        self.normalize()

    def __repr__(self):
        return "Gen: {:3d} / {:3d}: {:3d}| {}".format(
            self.generation, self.answer(), self.index_offset, self.pots
        )


tg = test_garden = Garden(*parse(test_data))


def r():
    global tg, test_garden
    tg = test_garden = Garden(*parse(test_data))


def test_first():
    print(tg)
    for i in range(0, 20):
        tg.tick()
        print(tg)


def first():
    garden = Garden(*parse(data))
    print(garden)
    for i in range(0, 20):
        garden.tick()
        print(garden)


def second():
    # Look for a stable pattern. Or fixpoint, if we're fancy.
    garden = Garden(*parse(data))
    found = False
    prev_pots = None
    while not found:
        garden.tick()
        found = prev_pots == garden.pots
        prev_pots = garden.pots
        if garden.generation % 10 == 0:
            print(garden)
    print(88 * '*')
    print(garden)

    # Only changes now are in the offset value
    # Let's make sure they are linear changes
    old_offset = garden.index_offset
    garden.tick()
    delta = garden.index_offset - old_offset
    old_offset = garden.index_offset
    for i in range(0, 10):
        garden.tick()
        assert (garden.index_offset - old_offset) == delta
        delta = garden.index_offset - old_offset
        old_offset = garden.index_offset
        print(garden)

    # So.  Offsets go up linearly and pot patterns stay the same.
    # Which means we have F(generation) => offset
    # Offset for generagion g, off_g given some gen0, off0 is
    #  off_g = (g - gen0) * delta + off0

    # Let's try to predict a future value.
    off0 = garden.index_offset
    gen0 = garden.generation
    print("off0, gen0, delta: ".format(off0, gen0, delta))

    g = 50000000000
    off_g = (g - gen0) * delta + off0
    print("Future offset: {}".format(off_g))
    garden.index_offset = off_g
    print("Future value: {}".format(garden.answer()))
