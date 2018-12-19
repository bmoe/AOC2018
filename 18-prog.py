import sys
import collections

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


def show():
    for y in range(0, leny):
        for x in range(0, lenx):
            sys.stdout.write(grid[x, y])
        sys.stdout.write('\n')
    print('\nTime: {}'.format(minute))
    kinds = dict(count_kinds())
    print('Counts: {}'.format(kinds))
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
