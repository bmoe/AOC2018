import itertools
import sys

grid = {}
# active_points = []
drips = []
min_x = None
max_x = None
min_y = None
max_y = None

BLUE = '\033[94m'
GREEN = '\033[92m'
END = '\033[0m'


data = open('17-input', 'r')
test = open('17-input-test', 'r')


def parse_junk(junk):
    c, vals = junk.split('=')
    if '.' in vals:
        low, high = map(int, vals.split('..'))
        vals = range(low, high + 1)
    else:
        vals = [int(vals)]
    return c, vals


def point(x, y):
    return grid.get((x, y), '.')


def load(inp):
    global grid
    # global active_points
    global drips
    global min_x, max_x
    global min_y, max_y

    grid = {}

    for line in inp:
        a, b = line.split(',')
        a = a.strip()
        b = b.strip()
        ac, avals = parse_junk(a)
        bc, bvals = parse_junk(b)
        if ac == 'x':
            xvals = avals
            yvals = bvals
        else:
            yvals = avals
            xvals = bvals

        for coord in itertools.product(xvals, yvals):
            grid[coord] = '#'

    xs, ys = zip(*grid.keys())
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)

    # Set water
    water_point = (500, 0)
    grid[water_point] = '+'
    # active_points = [water_point]
    drips = [water_point]


def show():
    for y in range(0, max_y + 2):
        for x in range(min_x - 1, max_x + 2):
            ch = grid.get((x, y), '.')
            if (x, y) in drips:
                ch = GREEN + ch + END
            elif ch in ['|', '~']:
                ch = BLUE + ch + END
            sys.stdout.write(ch)
        sys.stdout.write('\n')


def spread(x, y):
    # Try to spread out.
    # Are we constrained on the left and right?
    # Are we in a place that can hold water?
    left = x - 1
    right = x + 1

    constrained = True

    while point(left, y) != '#':
        if point(left, y+1) in ['.', '|']:
            constrained = False
            break
        left -= 1

    while point(right, y) != '#':
        if point(right, y+1) in ['.', '|']:
            constrained = False
            break
        right += 1

    return constrained, left, right


def tick():
    if not drips:
        return

    x, y = drips.pop()

    # go find where we stop dripping

    ybot = y + 1
    while point(x, ybot+1) == '.' and ybot <= max_y:
        grid[x, ybot] = '|'
        ybot += 1

    if ybot > max_y:
        return

    if point(x, ybot+1) == '|':
        # We've hit running water -- part of another drip. We stop.
        print('hit another drip')
        grid[x, ybot] = '|'
        return

    constrained, left, right = spread(x, ybot)
    # print(x, ybot)
    # print(constrained, left, right)

    while constrained:
        # left and right are clay. don't fill those in
        for x1 in range(left+1, right):
            grid[x1, ybot] = '~'
        ybot -= 1  # raise the floor
        constrained, left, right = spread(x, ybot)

    # Where are we dripping now?
    if point(left, ybot) != '#':
        drips.append((left, ybot))
    if point(right, ybot) != '#':
        drips.append((right, ybot))

    # Fill in drippy water
    for x in range(left, right+1):
        if point(x, ybot) != '#':
            grid[x, ybot] = '|'

    return True


def score(water):
    count = 0
    for x, y in grid.keys():
        if y >= min_y and y <= max_y:
            if point(x, y) in water:
                count += 1
    return count


def first(data):
    load(data)
    while drips:
        tick()
    show()
    return score(['|', '~'])


def second(data):
    load(data)
    while drips:
        tick()
    show()
    return score(['~'])
