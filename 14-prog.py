

# [(input, expected)]
test_data = [
    (5, '0124515891'),
    (9, '5158916779'),
    (18, '9251071085'),
    (2018, '5941429882'),
]

data = 540391


class Board:
    def __init__(self):
        self.scoreboard = [3, 7]
        self.nrecipies = len(self.scoreboard)

        # elf positions
        self.a = 0
        self.b = 1

    def tick(self):
        a_score = self.scoreboard[self.a]
        b_score = self.scoreboard[self.b]
        new_recipes = [int(ch) for ch in str(a_score+b_score)]

        self.scoreboard.extend(new_recipes)
        self.nrecipies += len(new_recipes)

        self.a = (self.a + a_score + 1) % self.nrecipies
        self.b = (self.b + b_score + 1) % self.nrecipies

    def __repr__(self):
        elf = {self.a: '.', self.b: ','}
        return(''.join([
            '{:3d}{}'.format(r, elf.get(i, ' '))
            for i, r in enumerate(self.scoreboard)
        ]))


def bake(ntrials):
        b = Board()
        while b.nrecipies < ntrials + 10:
            b.tick()
        return ''.join(map(str, b.scoreboard[ntrials:ntrials+10]))


def first_test():
    for inp, expected in test_data:
        result = bake(inp)
        if result != expected:
            print("{} != expected {}").format(result, expected)
        else:
            print('Cool')


def first():
    print(bake(data))
