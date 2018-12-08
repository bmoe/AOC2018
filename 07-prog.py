import collections


def parse(lines):
    # [str] -> [(str, str)]
    return map(parse_line, lines)


def parse_line(line):
    d = line.split()
    return d[1], d[7]


test_input = list(map(parse_line, """
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
""".strip().split('\n')))


def real_input():
    for line in open('07-input', 'r').readlines():
        line = line.strip()
        if line:
            yield parse_line(line)


class Graph:

    def __init__(self, edges=None):
        self._nodes = set()
        self._edges = collections.defaultdict(set)
        self._revedges = collections.defaultdict(set)

        edges = edges or []
        for edge in edges:
            self.add_edge(*edge)

    def nodes(self):
        return self._nodes

    def add_edge(self, a, b):
        self._nodes.add(a)
        self._nodes.add(b)
        self._edges[a].add(b)
        self._revedges[b].add(a)

    def successors(self, a):
        rv = set(self._edges[a])
        for node in self._edges[a]:
            rv = rv.union(self.successors(node))
        return rv

    def predecessors(self, a):
        rv = set(self._revedges[a])
        for node in self._revedges[a]:
            rv = rv.union(self.predecessors(node))
        return rv

    def remove_node(self, a):
        self._nodes.remove(a)
        if a in self._edges:
            if a in self._edges:
                del self._edges[a]
        if a in self._revedges:
            if a in self._revedges:
                del self._revedges[a]
        for n in self._edges.values():
            if a in n:
                n.remove(a)
        for n in self._revedges.values():
            if a in n:
                n.remove(a)

    def first_nodes(self):
        return sorted([
            node
            for node in self.nodes()
            if not self.predecessors(node)
        ])


def first(data):
    g = Graph(data)

    ready_guys = sorted(g.first_nodes())
    done_guys = []

    while ready_guys:
        this_guy = ready_guys.pop(0)
        done_guys.append(this_guy)
        g.remove_node(this_guy)
        ready_guys = sorted(g.first_nodes())

    assert not g.nodes()

    # GBDFHEIJKANPCORTVMUWQSXLYZ is wrong  :-(
    # GKPTSLUXBIJMNCADFOVHEWYQRZ

    return ''.join(done_guys)


class Elf:
    def __init__(self, name):
        self.name = name
        self.work = None
        self.t = 0
        # print('I am elf {}'.format(name))

    def take_work(self, work, t):
        # print('Elf {} working on task {} for {}s'.format(self.name, work, t))
        self.work = work
        self.t = t

    def is_idle(self):
        return self.t <= 0

    def tick(self):
        self.t -= 1
        # print('Elf {} on task {} has {}s left'.format(
        #     self.name, self.work, self.t)
        # )


def second(data, nelves=5, timepad=60):

    def task_size(task):
        return ord(task) - ord('A') + timepad + 1

    # omfg
    g = Graph(data)

    all_elves = [Elf(i) for i in range(0, nelves)]
    idle_elves = list(all_elves)
    working_elves = []

    inprogress_tasks = []
    workable_tasks = g.first_nodes()

    t = 0
    while True:

        print('{:05d} {}'.format(
            t,
            ' '.join([
                elf.work or '.' for elf in all_elves
            ])
        ))

        # Sweep up elves that are done
        finished = [elf for elf in working_elves if elf.is_idle()]
        if finished:
            pass
            # print('These jerks finished: {}'.format(
            #     [elf.name for elf in finished]))
        for elf in finished:
            working_elves.remove(elf)
            inprogress_tasks.remove(elf.work)
            g.remove_node(elf.work)
            elf.work = None
            idle_elves.append(elf)

        workable_tasks = g.first_nodes()

        # Load up available elves with ready work.
        for task in workable_tasks:
            # Make sure nobody is doing this task already
            # And that there are guys who can do work
            if idle_elves and (task not in inprogress_tasks):
                # Farm this bastard out
                elf = idle_elves.pop()
                elf.take_work(task, task_size(task))
                working_elves.append(elf)
                inprogress_tasks.append(task)

        # Are we done?
        if not working_elves:
            break

        # Beat the drum
        t += 1
        [elf.tick() for elf in working_elves]

    # 920
    print('Done in {}'.format(t))


x = """
Fri Dec  7 22:53:34 CST 2018
 7   7377   2546  *******
 6  11678    621  *********
 5  18419    762  **************
 4  18833    705  **************
 3  27027   1486  ********************
 2  36698   4253  ****************************
 1  47217  12475  *****************************************
"""
