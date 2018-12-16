import re
import collections

OPCODES = ['addr',
           'addi',
           'mulr',
           'muli',
           'banr',
           'bani',
           'borr',
           'bori',
           'setr',
           'seti',
           'gtir',
           'gtri',
           'gtrr',
           'stir',
           'stri',
           'strr',]


class Registers:
    def __init__(self, initial=None):
        self.regs = {i: val for i, val in enumerate(initial or [])}

    def get(self, rno):
        return self.regs.get(rno, 0)

    def set(self, rno, val):
        self.regs[rno] = val

    def __eq__(self, other):
        # Only works if the regs are fully iinitialized
        # ie they don't rely on that get() default
        return self.regs == other.regs
    def __repr__(self):
        return str(self.regs)

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

    elif op == 'stir':
        v = 1 if ai == r.get(bi) else 0
        r.set(co, v)
    elif op == 'stri':
        v = 1 if r.get(ai) == bi else 0
        r.set(co, v)
    elif op == 'strr':
        v = 1 if r.get(ai) == r.get(bi) else 0
        r.set(co, v)
    else:
        raise Exception('Unknown opcopde {}'.format(op))


def first(inp):
    if hasattr(inp, 'readlines'):
        lines = iter(map(lambda line: line.strip('\n'), inp.readlines()))
    else:
        lines = iter(inp.split('\n'))

    pat = re.compile(r'.*:\s*(\[\d+(,\s*\d+)+\])')
    init = next(lines)
    # mystery opcode number => # passing tests
    # tests = {}
    sample_count = 0
    # tests = collections.defaultdict(lambda: 0)
    while init:
        init_state = eval(re.match(pat, init).group(1))

        instr = next(lines)
        instr = map(int, instr.split())
        assert len(instr) == 4, "bad instr input '{}'".format(instr)

        expect = next(lines)
        expected = Registers(eval(re.match(pat, expect).group(1)))
        assert next(lines) == ''

        opnum = instr[0]
        op_args = instr[1:]
        same_count = 0
        for opcode in OPCODES:
            r = Registers(init_state)
            execute(opcode, *op_args + [r])
            if r == expected:
                same_count += 1
                if same_count >= 3:
                    sample_count += 1
                    break

        init = next(lines)

    return sample_count
