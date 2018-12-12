import collections
import time
import sys


def power(serial, x, y):
    rack_id = x + 10
    power = (rack_id * y) + serial
    power *= rack_id
    power = (power / 100) % 10
    return power - 5


def power_grid(serial, nx=300, ny=300):
    grid = collections.defaultdict(lambda: 0)
    for x in range(1, nx + 1):
        for y in range(1, ny + 1):
            grid[(x, y)] = power(serial, x, y)
    return grid


def three_bys(power, nx=300, ny=300):
    grid = collections.defaultdict(lambda: 0)
    for x in range(1, nx - 1):
        for y in range(1, ny - 1):
            for i in range(0, 3):
                for j in range(0, 3):
                    grid[(x, y)] += power[(x+i, y+j)]
    return grid


def max_guy(grid):
    max_val = grid.values()[0]
    max_index = None
    for index, value in grid.items():
        if value > max_val:
            max_val = value
            max_index = index
    return max_val, max_index


assert power(8, 3, 5) == 4
assert power(57, 122, 79) == -5
assert power(39, 217, 196) == 0
assert power(71, 101, 153) == 4


def first(serial=7689):
    return max_guy(three_bys(power_grid(serial)))


def first_test():
    assert first(18) == (29, (33, 45))
    assert first(42) == (30, (21, 61))
    assert first(7689) == (31, (20, 37))
    print("Yay!")


def n_bys(power, nx=300, ny=300, n=3):
    grid = collections.defaultdict(lambda: 0)

    # 1 2 3 4 5 6 7 8
    # nx = 8  n = 3
    # max_x = 8 - (3-1)

    max_x = nx - (n - 1)
    max_y = ny - (n - 1)
    for x in range(1, max_x + 1):
        for y in range(1, max_y + 1):
            for i in range(0, n):
                for j in range(0, n):
                    grid[(x, y)] += power[(x+i, y+j)]
    return grid


def bad_second(serial):

    power = power_grid(serial)
    best_n = 1
    best_val, best_index = max_guy(power)

    for n in range(2, 300):
        this_val, this_index = max_guy(n_bys(power, n=n))
        if this_val > best_val:
            best_val = this_val
            best_index = this_index
            best_n = n
        print("Did {}".format(n))

    return best_n, best_val, best_index


"""
x,y 1x -> x,y
x,y 2x -> x,y 1x + x+1,y + x,y+1 + x+1,y+1
x,y 3x -> x,y 2x + sum[(x+2, y+i)] +
                   sum[(x+i, y+2)] + (x+2,y+2)  for i <- [0, 1]

x,y Nx -> x,y N-1x + sum[x+N, y+i] +
                     sum[(x+i, y+N)] + (x+N,y+N)  for i <- [0, N-1]
  for x, y in 1..300-N(ish)

   X X *
   X X *
   * * *

   X X X X X *
   X X X X X *
   X X X X X *
   X X X X X *
   X X X X X *
   * * * * * *

construct subs :: n_by -> (x, y) -> power
"""


def fringe_coordinates(n, x, y):
    return (
        [(x+i, y+n-1) for i in range(0, n-1)] +
        [(x+n-1, y+i) for i in range(0, n-1)] +
        [(x+n-1, y+n-1)]
    )


def subs(power, nx=300, ny=300, max_n=300):
    # sub1 is the 1x1 sub-grid, or just the power grid
    s = {1: power}
    for n in range(2, max_n+1):
        # Show progress -- I am impatient an distrustful
        sys.stdout.write('.')
        sys.stdout.flush()
        max_x = nx - (n - 1)
        max_y = ny - (n - 1)
        parent_grid = s[n-1]
        this_sub_grid = {}
        for x in range(1, max_x + 1):
            for y in range(1, max_y + 1):
                fringe_val = 0
                for coord in fringe_coordinates(n, x, y):
                    fringe_val += power[coord]
                here = (x, y)
                this_sub_grid[here] = parent_grid[here] + fringe_val
        s[n] = this_sub_grid
    return s


def show(g, x=10, y=10):
    for y in range(1, y+1):
        line = []
        for x in range(1, x+1):
            line.append("%3d" % g[(x, y)])
        print(' '.join(line))


def test_subs(serial):
    p = power_grid(serial)
    s = subs(p, max_n=3)
    assert p == s[1]
    assert three_bys(p) == s[3]


def second(serial=7689):
    # Oof. This thing takes like 10 minutes.
    start = time.time()
    p = power_grid(serial)
    s = subs(p)
    candidates = {k: max_guy(s[k]) for k in s.keys()}
    best_val = p.values()[0]  # just any value will do
    best_size = None
    best_index = None
    for size, (val, index) in candidates.items():
        if val >= best_val:
            best_val = val
            best_size = size
            best_index = index

    print(candidates[best_size])
    (val, (x, y)) = candidates[best_size]

    print("Best value {}".format(best_val))
    print("Best index {}".format(best_index))
    print("the data: {}".format(candidates[best_size]))
    print("This beast took {} seconds".format(time.time() - start))

    return("{},{},{}".format(x, y, best_size))


def second_test():
    test_data = [(18, "90,269,16"), (42, "232,251,12"), (7689, "90,169,15")]
    for (serial, expected) in test_data:
        actual = second(serial)
        if actual == expected:
            print("Serial {} PASSED".format(serial))
        else:
            print("Serial {} FAILED - {} != {}", format(
                serial, actual, expected))
