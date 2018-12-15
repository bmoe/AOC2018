
# [(input, expected)]
test_data = [
    (5, '0124515891'),
    (9, '5158916779'),
    (18, '9251071085'),
    (2018, '5941429882'),
]

test_data2 = [
    ("51589", 9),
    ("01245", 5),
    ("92510", 18),
    ("59414", 2018),
]

data = 540391


class Board:
    def __init__(self, target=None):
        self.scoreboard = []
        self.nrecipes = 0

        if target:
            target = [int(ch) for ch in target]
        else:
            target = [None]  # something we can never match
        self.target = target

        self.target_found = False
        self.target_found_after = None
        self.target_length = len(target)
        # Index we check against to see if we're matching
        self.target_to_match = 0

        # elf positions
        self.a = 0
        self.b = 1
        self.add_a_score(3)
        self.add_a_score(7)

    def add_a_score(self, score):
        # Add new recipes while checking if we hit the target
        self.nrecipes += 1
        self.scoreboard.append(score)
        if score == self.target[self.target_to_match]:
            # matching!
            self.target_to_match += 1
            if self.target_to_match >= self.target_length:
                # We found all the things!
                self.target_found = True
                self.target_found_after = self.nrecipes - len(self.target)
                # In case there is an extra recipe that we don't care about
                self.target_to_match = 0
        else:
            # Start over matching target
            self.target_to_match = 0
            if score == self.target[0]:
                self.target_to_match = 1
            # Very sloppy.  Will only work if we are lucky.
            # But I think we'll be lucky since there are no
            # repeats in our input

    def tick(self):
        a_score = self.scoreboard[self.a]
        b_score = self.scoreboard[self.b]
        new_recipes = [int(ch) for ch in str(a_score+b_score)]

        for new in new_recipes:
            self.add_a_score(new)

        self.a = (self.a + a_score + 1) % self.nrecipes
        self.b = (self.b + b_score + 1) % self.nrecipes
        return self

    def __repr__(self):
        elf = {self.a: '.', self.b: ','}
        return(''.join([
            '{:3d}{}'.format(r, elf.get(i, ' '))
            for i, r in enumerate(self.scoreboard)
        ]))


def bake(ntrials):
        b = Board('')
        while b.nrecipes < ntrials + 10:
            b.tick()
        return ''.join(map(str, b.scoreboard[ntrials:ntrials+10]))


def first_test():
    for inp, expected in test_data:
        result = bake(inp)
        if result != expected:
            print('{} != expected {}').format(result, expected)
        else:
            print('Cool')


def first():
    # 1474315445  1 second
    print(bake(data))


def second_test():
    for (pattern, expected) in test_data2:
        b = Board(pattern)
        while not b.target_found:
            b.tick()
        if b.target_found_after != expected:
            print('{} != expected {}').format(b.target_found_after, expected)
        else:
            print('Cool')


def second():
    b = Board(str(data))
    while not b.target_found:
        b.tick()
    print(b.target_found_after)
    # 20278122  39 seconds.  ugh.
