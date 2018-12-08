# I am sorry I do not differentiate between a string
# and a list of integers representing characters.
# They are all called 's' and I am a jerk for that.

import time


def react_one(s):
    for i in range(0, len(s) - 1):
        if abs(s[i] - s[i+1]) == 32:
            # Reaction! Remove these guys.
            return s[:max(0, i)] + s[min(len(s), i+2):]
    return s


def react(s):
    old_s = object()
    while old_s != s:
        old_s = s
        s = react_one(s)
    if old_s == s:
        return s


def first(s):
    s = map(ord, s)
    return len(react(s))


def remove(ch, s):
    removals = [ord(ch.upper()), ord(ch.lower())]
    return [c for c in s if c not in removals]


def second(s):
    orig = map(ord, s)
    all_letters = [chr(ch) for ch in range(ord('a'), ord('z') + 1)]

    actual_start = time.time()
    reactions = {}

    for ch in all_letters:
        s = remove(ch, orig)
        start = time.time()
        length = len(react(s))
        reactions[ch] = length
        duration = time.time() - start
        print('processed {} in {} seconds. len: {}'.format(
            ch, duration, length)
        )

    print('shortest polymer is: {}'.format(min(reactions.values())))
    print('total duration is: {} seconds'.format(time.time() - actual_start))
