import re
import sys
import time


def data():
    return open('19-input', 'r')


def test_data():
    return open('19-input-test', 'r')


class Registers:
    def __init__(self, initial):
        self._ip = None
        self.regs = initial

    def ip(self):
        return self.get(self._ip)

    def step(self):
        self.set(self._ip, self.ip() + 1)

    def get(self, rno):
        return self.regs[rno]

    def set(self, rno, val):
        self.regs[rno] = val

    def __eq__(self, other):
        return self.regs == other.regs

    def __repr__(self):
        return "ip={} {}".format(self.ip(), self.regs)


def execute(op, ai, bi, co, r):
    # 16 opcodes. man.
    if op == 'addr':
        r.set(co, r.get(ai) + r.get(bi))
    elif op == 'addi':
        r.set(co, r.get(ai) + bi)
    elif op == 'mulr':
        r.set(co, r.get(ai) * r.get(bi))
    elif op == 'muli':
        r.set(co, r.get(ai) * bi)

    elif op == 'banr':
        r.set(co, r.get(ai) & r.get(bi))
    elif op == 'bani':
        r.set(co, r.get(ai) & bi)
    elif op == 'borr':
        r.set(co, r.get(ai) | r.get(bi))
    elif op == 'bori':
        r.set(co, r.get(ai) | bi)

    elif op == 'setr':
        r.set(co, r.get(ai))
    elif op == 'seti':
        r.set(co, ai)

    elif op == 'gtir':
        v = 1 if ai > r.get(bi) else 0
        r.set(co, v)
    elif op == 'gtri':
        v = 1 if r.get(ai) > bi else 0
        r.set(co, v)
    elif op == 'gtrr':
        v = 1 if r.get(ai) > r.get(bi) else 0
        r.set(co, v)

    elif op == 'eqir':
        v = 1 if ai == r.get(bi) else 0
        r.set(co, v)
    elif op == 'eqri':
        v = 1 if r.get(ai) == bi else 0
        r.set(co, v)
    elif op == 'eqrr':
        v = 1 if r.get(ai) == r.get(bi) else 0
        r.set(co, v)
    else:
        raise Exception('Unknown opcopde {}'.format(op))


registers = None
prog = []


def load(data):
    global registers
    global prog

    try:
        data = data()
    except Exception:
        pass

    registers = Registers([0 for _ in range(0, 6)])
    prog = []

    first = next(data)
    ip = int(re.match('#ip(\s*\d+)', first).group(1))
    registers._ip = ip

    # load program
    for src_line in data:
        instr = src_line.strip().split(' ')
        instr = [instr[0]] + list(map(int, instr[1:]))
        prog.append(instr)


def first(data):
    load(data)

    start = time.time()
    tickno = 0

    r = registers
    while r.ip() < len(prog):
        # before = str(r)
        instr = prog[r.ip()]
        execute(*instr, r)
        # print('{} {} {}'.format(before, instr, r))
        r.step()
        tickno += 1
        if (tickno % 10000) == 0:
            sys.stdout.write('.')
            sys.stdout.flush()

    sys.stdout.write('\n')
    print('{} steps in {} seconds'.format(tickno, time.time() - start))
    print(r)
    # 6156552 steps in 18.436479091644287 seconds
    # ip=257 [878, 878, 877, 878, 1, 257]
