import collections
import sys

codes = [line.strip() for line in sys.stdin.readlines()]

twos = 0
threes = 0

for code in codes:
    counts = collections.defaultdict(lambda: 0)
    for ch in code:
        counts[ch] += 1
    count_sets = set(counts.values())
    if 2 in count_sets:
        twos += 1
    if 3 in count_sets:
        threes += 1

print("Checksum is {}".format(twos * threes))


def difference(a, b):
    assert len(a) == len(b)
    return sum([1 for (x, y) in zip(a, b) if x != y])


def find_close():
    for a in codes:
        for b in codes:
            if difference(a, b) == 1:
                return (a, b)
    return None


(a, b) = find_close()
print(
    "magic string is: {}"
    .format(''.join([ch1 for (ch1, ch2) in zip(a, b) if ch1 == ch2]))
)
