
import collections
import sys


class Claim:
    def __init__(self, key, xoff, yoff, xlen, ylen):
        self.key = key
        self.xoff = int(xoff)
        self.xlen = int(xlen)
        self.yoff = int(yoff)
        self.ylen = int(ylen)

    def squares(self):
        # The (x,y) squares this claim covers.
        return [
            (x, y)
            for x in range(self.xoff, self.xoff + self.xlen)
            for y in range(self.yoff, self.yoff + self.ylen)
        ]

    @classmethod
    def parse(cls, inp):
        # rashly assume all data is good and looks like this:
        # eg:  "#1 @ 906,735: 28x17"
        inp = inp.split()
        key = inp[0][1:]
        xoff, yoff = inp[2][:-1].split(',')
        xlen, ylen = inp[3].split('x')
        return cls(key, xoff, yoff, xlen, ylen)


# Get the claims
claims = [Claim.parse(line) for line in sys.stdin.readlines()]

# Count how many claims claim each square
cloth = collections.defaultdict(lambda: 0)
for claim in claims:
    for square in claim.squares():
        cloth[square] += 1

overlapping_sq_inches = sum([
    1
    for num_covering in cloth.values()
    if num_covering > 1
])

print('Number of sq inches with overlap is: {}'.format(overlapping_sq_inches))


# Look for a claim that has no overlap with another.
# It's squares will all have a claim count of 1 on the cloth.
for claim in claims:
    has_overlap = False  # optimism!
    for square in claim.squares():
        if cloth[square] > 1:
            # This is not the claim we are looking for
            has_overlap = True
    if not has_overlap:
        print('Claim #{} has no overlap'.format(claim.key))
