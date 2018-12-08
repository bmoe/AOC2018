import functools

test_input = """
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
""".strip().split('\n')


def real_input():
    for line in open('07-input', 'r').readlines():
        line = line.strip()
        if line:
            yield line


def parse(lines):
    # [str] -> [(str, str)]
    return map(parse_line, lines)


def parse_line(line):
    d = line.split()
    return d[1], d[7]


@functools.total_ordering
class Node:
    def __init__(self, name):
        self.name = name
        self._successors = []
        self._predecessors = []

    def make_edge(self, node):
        self._successors.append(node)
        node._predecessors.append(self)

    def successors(self):
        s = set(self._successors)
        for n in self._successors:
            s = s.union(n.successors())
        return s

    def __lt__(self, other):
        if self in other.successors:
            return False
        if other in self.successors:
            return True
        return self.name < other.name

    def __eq__(self, other):
        return self.name == other.name


class Graph:

    def __init__(self):
        # name -> Node
        self.nodes = {}

    def get_node(self, name):
        if name not in self.nodes:
            self.nodes[name] = Node(name)
        return self.nodes[name]

    def all_nodes(self):
        return self.nodes.values()


def build_nodes(orderings):
    # [(str, str)] -> Graph
    g = Graph()
    for a, b in orderings:
        a = g.get_node(a)
        b = g.get_node(b)
        a.make_edge(b)

    return g


def first(data):
    orders = parse(data)
    g = build_nodes(orders)
    return g


def garbage():
    # All the nodes
    nodes = g.all_nodes()

    all_successors = [
        s
        for succs in [n.successors for n in g.all_nodes()]
        for s in succs
    ]

    first_guys = [guy for guy in nodes if guy not in all_successors]

    ready_guys = sorted(first_guys)
    done_guys = []

    while True:
        if len(ready_guys) == 0:
            break
        this_guy = ready_guys.pop(0)

        ready_guys.sort()  # dirty!

    # GBDFHEIJKANPCORTVMUWQSXLYZ is wrong
    return ''.join(done_guys)
