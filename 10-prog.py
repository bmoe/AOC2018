import re
import sys

test_file = '10-input-test'
data_file = '10-input'

# Python version shenanigans
try:
    raw_input  # noqa
except NameError:
    raw_input = input


def parse(data):
    pat = re.compile(
        r'position=<([^,]+),([^>]+)> *velocity=<([^,]+),([^>]+)>.*'
    )
    return [map(int, pat.match(line).groups()) for line in data]


class UFO:
    def __init__(self, x, y, xv, yv):
        self.x, self.y = x, y
        self.xv, self.yv = xv, yv

    def move(self, nsec):
        self.x += nsec * self.xv
        self.y += nsec * self.yv


class Sky:
    def __init__(self, ufos):
        self.ufos = ufos
        self.time = 0

    def move(self, nsec=1):
        self.time += nsec
        map(lambda x: x.move(nsec), self.ufos)

    def map(self):
        return {(ufo.x, ufo.y): True for ufo in self.ufos}

    def ranges(self):
        x0, xn, y0, yn = self.maxes()
        return (xn - x0, yn - y0)

    def maxes(self):
        maxx = minx = self.ufos[0].x
        miny = maxy = self.ufos[0].y
        for ufo in self.ufos:
            minx, maxx = min(ufo.x, minx), max(ufo.x, maxx)
            miny, maxy = min(ufo.y, miny), max(ufo.y, maxy)
        return minx, maxx, miny, maxy

    def show(self, x0, xn, y0, yn):
        map = self.map()
        for y in range(y0, yn+1):
            for x in range(x0, xn+1):
                if (x, y) in map:
                    sys.stdout.write('*')
                else:
                    sys.stdout.write(' ')
            sys.stdout.write('\n')


def explore(fname):
    """ Browse around time and find the message in the stars.
    """
    datas = parse(open(fname, 'r').readlines())
    sky = Sky([
       UFO(*data) for data in datas
    ])

    an_ufo = [ufo for ufo in sky.ufos if ufo.xv != 0][0]  # get a moving one!
    guess = an_ufo.x / an_ufo.xv
    print('One guy gets to zero at about {} seconds. Just sayin'.format(
            guess))

    # Prompt shows time t, and the magnitude of x and y ranges.
    # Which is basically the size of the sky.
    # If all the stars in in the message, the message will appear
    # sometime around the minimum of those ranges.

    cmd = raw_input('{}/{} - '.format(sky.time, sky.ranges())).strip()
    while cmd not in ['q', 'Q']:

        if cmd == 's':  # Careful!
            sky.show(*sky.maxes())
        if cmd == 'm':
            print(sky.maxes())
        if cmd.startswith('g'):  # move in time!
            seconds = int(cmd[1:])
            sky.move(seconds)

        # Show the sky when the sky is small enough.
        if cmd == '-':  # back one second
            sky.move(-1)
            xr, yr = sky.ranges()
            if xr < 200 and yr < 200:
                sky.show(*sky.maxes())
        if cmd == '':  # forward one second
            sky.move()
            xr, yr = sky.ranges()
            if xr < 200 and yr < 200:
                sky.show(*sky.maxes())
        cmd = raw_input('{}/{} - '.format(sky.time, sky.ranges())).strip()
    print('Bye!')
