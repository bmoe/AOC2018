import collections
import time


def pointify(lines):
    p = []
    for line in lines:
        x, y = line.split(',')
        p.append((int(x), int(y)))
    return p


test_points = pointify("""
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
""".strip().split('\n'))


points = pointify(
    open('06-input', 'r').readlines()
)


def distance(a, b):
    ax, ay = a
    bx, by = b
    return abs(ax - bx) + abs(ay - by)


def grid_boundaries(ps):
    xs = map(lambda p: p[0], ps)
    ys = map(lambda p: p[1], ps)

    x0 = min(xs) - 1
    xn = max(xs) + 1
    y0 = min(ys) - 1
    yn = max(ys) + 1

    print('Grid area is: {}'.format((xn-x0)*(yn-y0)))

    return (x0, xn), (y0, yn)


def edge_points(m):
    x0, xn = min([p[0] for p in m.keys()]), max([p[0] for p in m.keys()])
    y0, yn = min([p[1] for p in m.keys()]), max([p[1] for p in m.keys()])

    for x in range(x0, xn+1):
        yield (x, y0)
        yield (x, yn)
    for y in range(y0, yn+1):
        yield (x0, y)
        yield (xn, y)


def raw_distance_map(points):
    # m[gridpoint] -> (dist, [point])
    # Points w/ least distance seen
    m = {}
    point_index = {
        point: i
        for (i, point) in enumerate(points)
    }
    print('Names: {}'.format(point_index))
    (x0, xn), (y0, yn) = grid_boundaries(points)
    for x in range(x0, xn+1):
        for y in range(y0, yn+1):
            here = (x, y)
            for point in points:
                pname = point_index[point]
                # is p a winner?
                fromhere = distance(here, point)
                if here not in m:
                    # first to measure!  an easy win.
                    m[here] = (fromhere, [pname])
                else:
                    winning, winners = m[here]
                    if fromhere < winning:
                        # solo winner yay!
                        m[here] = (fromhere, [pname])
                    elif fromhere == winning:
                        # tied with some guy(s)
                        winners.append(pname)
    return m


def prune_map(m):
    # (point -> (dist, [points])) -> (point -> maybe point)
    for here in m.keys():
        winning, winners = m[here]
        if len(winners) == 1:
            m[here] = winning, winners[0]
        else:
            m[here] = None
    return m


def find_inner_guys(m):
    # m:: gridpoint -> maybe (d, p)
    #
    # We want all (d, p) guys who have no presence on an edge.
    # So let's find all p values that exist on the edge

    edge_ps = set()
    for p in edge_points(m):
        if m[p]:
            edge_ps.add(m[p][1])

    print(edge_ps)

    # Now count instances of (_, p) for all p that are not edge p's.
    inners = collections.defaultdict(lambda: 0)
    for guy in m.values():
        if guy is not None and guy[1] not in edge_ps:
            inners[guy[1]] += 1

    return inners


def print_map(m):
    x0, xn = min([p[0] for p in m.keys()]), max([p[0] for p in m.keys()])
    y0, yn = min([p[1] for p in m.keys()]), max([p[1] for p in m.keys()])

    for y in range(y0, yn+1):
        row = []
        for x in range(x0, xn+1):
            v = m[(x, y)]
            if v is None:
                ch = '.'
            else:
                ch = v[1]
            row.append('{}'.format(ch))
        print(''.join(row))


def first(points):
    print('Generating raw distances')
    real_start = start = time.time()
    m = raw_distance_map(points)
    print('  {} seconds'.format(time.time() - start))

    print('Pruning')
    start = time.time()
    m = prune_map(m)
    print('  {} seconds'.format(time.time() - start))

    print('Finding Innger Guys')
    start = time.time()
    winners = find_inner_guys(m)
    print('  {} seconds'.format(time.time() - start))

    print('Here they are!')
    print(winners)

    print('Finding inner point with largest area')
    print('Code: {}'.format(max(winners.values())))

    print('Total time: {} seconds'.format(time.time() - real_start))


def raw_map2(points, safety_margin):
    m = {}
    point_index = {
        point: i
        for (i, point) in enumerate(points)
    }
    print('Names: {}'.format(point_index))
    (x0, xn), (y0, yn) = grid_boundaries(points)
    for x in range(x0, xn+1):
        for y in range(y0, yn+1):
            here = (x, y)
            dsum = 0
            for p in points:
                dsum += distance(here, p)
            if dsum < safety_margin:
                m[here] = (0, '+')
            else:
                m[here] = None
    return m


def second(points, r):
    m = raw_map2(points, r)
    # print_map(m)

    # There is a risk that the grid we picked to search is too small.
    # If all the edges are not "safe" then the grid we searched was big enough.
    # Let's do a reality_check

    safe_edge_points = [p for p in edge_points(m) if m[p] is not None]
    assert len(safe_edge_points) == 0

    code = len([p for p in m.values() if p is not None])
    print('Code: {}'.format(code))
