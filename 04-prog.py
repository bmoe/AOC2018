import collections
import datetime
import functools
import itertools
import operator

# Example Input
#
# [1518-06-25 23:58] Guard #1069 begins shift
# [1518-09-16 00:24] falls asleep
# [1518-04-06 00:56] wakes up
# [1518-11-04 00:48] wakes up


def parse_date(dstr):
    # print('parsing "{}"'.format(dstr))
    return datetime.datetime.strptime(dstr, '[%Y-%m-%d %H:%M]')


def parse_line(line):
    return (parse_date(line[0:18]), line[19:-1])


def lines_from_file(fname):
    return [parse_line(line)
            for line in sorted(open(fname).readlines())]


fake = """[1518-06-27 23:58] Guard #1069 begins shift
[1518-06-27 00:24] falls asleep
[1518-06-27 00:56] wakes up
[1518-06-25 23:58] Guard #1069 begins shift
[1518-06-25 00:14] falls asleep
[1518-06-25 00:18] wakes up""".split('\n')


def real():
    return sorted(open('04-input', 'r').readlines())


class Hour:
    def __init__(self):
        self.hour = list(itertools.repeat(0, 60))

    def sleep(self, minute):
        self.sleepstart = minute

    def wake(self, minute):
        assert self.sleepstart < minute
        for i in range(self.sleepstart, minute):
            self.hour[i] = 1
        self.sleepstart = None

    def slept_for(self):
        return sum(self.hour)


def guards(data):
    # guards[guard_id][date]
    guards = collections.defaultdict(lambda: collections.defaultdict(Hour))

    guard_id = None
    for (date, action) in data:
        if action.startswith('Guard'):
            guard_id = int(action[7:].split()[0])
        elif action.startswith('falls'):
            # print('guard {} sleeps at {} {}'.format(
            #     guard_id, date.minute, date))
            assert guard_id
            guards[guard_id][date.isocalendar()].sleep(date.minute)
        elif action.startswith('wakes'):
            # print('guard {} wakes at {} {}'.format(
            #     guard_id, date.minute, date))
            assert guard_id
            guards[guard_id][date.isocalendar()].wake(date.minute)

    return guards


def longest_sleeper(guards):
    minutes_slept = {}

    for guard_id, guard_days in guards.items():
        minutes_slept[guard_id] = sum(
            [day.slept_for() for day in guard_days.values()]
        )

    slept = minutes_slept

    longest_sleep = max(slept.values())
    for guard, sleeptime in slept.items():
        if sleeptime == longest_sleep:
            return guard


def minute_map(hours):
    return functools.reduce(
        lambda a, b: map(operator.add, a, b),
        [h.hour for h in hours]
    )


def hot_minute(hours):
    """Given a list of hours, return the minute that was slept in most
    """
    minute_sums = minute_map(hours)
    # minute_sums = functools.reduce(
    #     lambda a, b: map(operator.add, a, b),
    #     [h.hour for h in hours]
    # )
    best_minute_total = max(minute_sums)
    for i, m in enumerate(minute_sums):
        if m == best_minute_total:
            return i, best_minute_total


def first(lines):
    g = guards(map(parse_line, lines))
    guard = longest_sleeper(g)
    print('sleepy guard: {}'.format(guard))
    print('his hours: {}'.format(g[guard].values()))
    hot = hot_minute(g[guard].values())[0]
    print('Guard: {} Minute: {} Code: {}'.format(guard, hot, guard * hot))


def second(lines):
    g = guards(map(parse_line, lines))

    # gid -> vector[min -> total]
    g_hours = {
        gid: hot_minute(g[gid].values())
        for gid in g
    }

    # want the guard with the biggest hot minute

    print(g_hours.items())

    gid, (minute, value) = max(
        *g_hours.items(),
        # arg looks like: (gid, (minute, value))
        # we want to key off of value
        key=lambda gid_minute_value: gid_minute_value[1][1]
    )

    print('gid: {} minute: {} val: {}'.format(gid, minute, value))
    print('code: {}'.format(gid * minute))
