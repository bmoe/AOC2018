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


def second(inp):
    if hasattr(inp, 'readlines'):
        lines = iter(map(lambda line: line.strip('\n'), inp.readlines()))
    else:
        lines = iter(inp.split('\n'))

    pat = re.compile(r'.*:\s*(\[\d+(,\s*\d+)+\])')
    init = next(lines)
    # Figure out opcode mappings  opcode <-> opnum
    # Ultimately want opnum -> opcode

    fails = collections.defaultdict(set)
    while init:
        # Go through each test seeing which ones pass
        # for which opecodes
        init_state = eval(re.match(pat, init).group(1))

        instr = next(lines)
        instr = map(int, instr.split())
        assert len(instr) == 4, "bad instr input '{}'".format(instr)

        expect = next(lines)
        expected = Registers(eval(re.match(pat, expect).group(1)))
        assert next(lines) == ''

        opnum = instr[0]
        op_args = instr[1:]

        for opcode in OPCODES:
            r = Registers(init_state)
            execute(opcode, *op_args + [r])

            # Start ruling out / accepting
            # whether opecode is represented by opnum
            if r == expected:
                # Ugh.  I don't feel like finding out if I have
                # to implement __ne__ or __neq__
                pass
            else:
                fails[opnum].add(opcode)

        init = next(lines)

    # Now we have a list of test failures
    # Let's construct opnum -> [opcode] -- possible mappings
    assert len(fails) in [15, 16]
    possibles = {}
    for opnum in range(0, 16):
        possibles[opnum] = set(OPCODES) - fails[opnum]
    print(possibles)

    # This is the mapping we want -- construct it
    # (why such a dumb name?)
    numcodemap = {}

    i = 0
    while possibles and i < 16:
        i += 1
        newguys = []
        for opnum, candidates in possibles.items():
            if len(candidates) == 1:
                newguys.append((opnum, candidates.pop()))
        for (opnum, code) in newguys:
            numcodemap[opnum] = code
            # Nobody else can claim this code
            for codes in possibles.values():
                if code in codes:
                    codes.remove(code)
            # Stop trying to map the opnum
            del possibles[opnum]

    assert not possibles

    # Run the program
    r = Registers()
    for srctext in lines:
        if not srctext:
            print("BLANK")
            continue

        progline = map(int, srctext.split())
        opcode = numcodemap[progline[0]]
        op_args = progline[1:]
        execute(opcode, *op_args + [r])

    print(r)
    return r.get(0)
