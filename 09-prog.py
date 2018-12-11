
import collections


try:
    range = xrange  # noqa
except Exception:
    pass


class Game:
    def __init__(self, nplayers):
        self.circle = collections.deque([0])
        self.mod = 1  # number of things in circle. can do len(), but.. O(?)
        self.nplayers = nplayers
        self.next_marble = 1
        self.scores = collections.defaultdict(lambda: 0)

    def rotate(self, n):
        self.marbles.rotate(n)

    def step(self):
        this_marble = self.next_marble
        if this_marble % 23 != 0:
            # add a marble
            self.circle.rotate(1)
            self.circle.appendleft(this_marble)
        else:
            # score
            self.circle.rotate(-7)
            removed_marble = self.circle.popleft()
            this_elf = this_marble % self.nplayers
            self.scores[this_elf] += removed_marble + this_marble
            self.circle.rotate(1)

        self.next_marble += 1
        return self

    def __repr__(self):
        return("{}\n{}".format(self.scores, self.circle))

    def play(self, num_marbles):
        for _ in range(0, num_marbles+1):
            self.step()
        return self

    def highest_score(self):
        return max(self.scores.values())


def go(elves, stones):
    return Game(elves).play(stones).highest_score()


def test():
    data = [
        (10, 1618, 8317),
        (13, 7999, 146373),
        (17, 1104, 2764),
        (21, 6111, 54718),
        (30, 5807, 37305),
    ]

    t = 0
    for (elves, marbles, expected) in data:
        t += 1
        res = go(elves, marbles)
        if res == expected:
            print("Test {} passed".format(t))
        else:
            print("Test {} failed. {} != {}".format(t, res, expected))


# Test data
# 403 players; last marble is worth 71920 points

def first():
    return go(403, 71920)


def second():
    return go(403, 71920 * 100)
