import collections
import time

data = open('18-input', 'r')
test = open('18-input-test', 'r')

TREE = '|'
LUMBERYARD = '#'
OPEN = '.'


grid = None
lenx = None
leny = None
minute = 0


def load(data):
    global grid
    global lenx
    global leny
    global minute

    grid = collections.defaultdict(lambda: None)
    lenx = 0
    leny = 0
    minute = 0
    for y, row in enumerate(data):
        leny += 1
        lenx = 0
        for x, ch in enumerate(row.strip()):
            grid[x, y] = ch
            lenx += 1  # yea, redundant and dumb.


def snapshot():
    # grid -> string
    lines = []
    for y in range(0, leny):
        lines.append(''.join([(grid[x, y]) for x in range(0, lenx)]))
    return '\n'.join(lines)


def score():
    kinds = count_kinds()
    return kinds[TREE] * kinds[LUMBERYARD]


def show():
    print()
    print(snapshot())
    # for y in range(0, leny):
    #     for x in range(0, lenx):
    #         sys.stdout.write(grid[x, y])
    #     sys.stdout.write('\n')
    print('\nTime: {}'.format(minute))
    kinds = count_kinds()
    print('Counts: {}'.format(dict(kinds)))
    print('Score: {}'.format(kinds[TREE] * kinds[LUMBERYARD]))


def count_kinds():
    # Count all squares by type
    rv = collections.defaultdict(lambda: 0)
    for y in range(0, leny):
        for x in range(0, lenx):
            rv[grid[x, y]] += 1
    return rv


def neighbor_kinds(x, y):
    # Count neighbors by type
    rv = collections.defaultdict(lambda: 0)
    for y1 in range(y-1, y+2):
        for x1 in range(x-1, x+2):
            if x1 == x and y1 == y:
                continue
            ch = grid[x1, y1]
            if ch:
                rv[ch] += 1
    return rv


def tick():
    global grid
    global minute

    next_grid = collections.defaultdict(lambda: None)
    minute += 1

    for y in range(0, leny):
        for x in range(0, lenx):
            this_acre = grid[x, y]
            counts = neighbor_kinds(x, y)

            # Assume nothing happens
            next_grid[x, y] = this_acre

            if this_acre == OPEN and counts[TREE] >= 3:
                next_grid[x, y] = TREE

            elif this_acre == TREE and counts[LUMBERYARD] >= 3:
                next_grid[x, y] = LUMBERYARD

            elif this_acre == LUMBERYARD:
                if not counts[LUMBERYARD] or not counts[TREE]:
                    next_grid[x, y] = OPEN

    grid = next_grid


def first(data):
    load(data)
    show()
    for _ in range(0, 10):
        tick()
    show()
    # 486878


def second(data):
    start = time.time()
    load(data)

    # Wait until we are in cycle land.
    # Determined by running and watching.
    for _ in range(0, 500):
        tick()
    print('Priming finished. {} seconds'.format(time.time() - start))

    scores = {}
    snapshots = {}
    snapshots[snapshot()] = minute
    scores[minute] = score()

    while True:
        tick()
        snap = snapshot()
        if snap in snapshots:
            break
        snapshots[snap] = minute
        scores[minute] = score()

    print(scores)
    print('cycle length is {} (ish)'.format(len(snapshots)))
    print('took {} seconds'.format(time.time() - start))

    # score at 500 is scores[0]
    # cycle = len(scores)
    # score at N is scores[ N-500 % cycle ] + 500
    # so score at 1000000000 is
    # 190836, 7.3s
    print(scores[((1000000000-500) % len(scores)) + 500])
