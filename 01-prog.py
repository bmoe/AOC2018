import sys
import operator
import functools

vals = [int(x) for x in sys.stdin.readlines()]
print(functools.reduce(operator.add, vals, 0))

seen = {}

last = 0
seen[last] = True
cycle = 1
while True:
    for v in vals:
        last = last + v
        if last in seen:
            print(
                    '{} is the guy during cycle {}'
                    .format(last, cycle)
            )
            sys.exit(0)
        seen[last] = True
    cycle += 1

print('o what?')
