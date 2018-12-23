
# """

# (EEEE(NNN|SS(EE|N)))

# E,E,E,E,(,N,N,N,|,S,S,(,E,E,|,N,),),
# [e,e,e,e,[[n,n,n],[s,s,[[e,e],[n]]]]

# """

import pyparsing as p


class Branch:
    def __init__(self, things):
        self.things = things

    def __repr__(self):
        return '(' + '|'.join([str(t) for t in self.things]) + ')'
        # return 'B<{}>'.format(self.things)


# UNKNOWN = None
# DOOR = '|'
# WALL = '#'

LPAR = p.Suppress('(')
RPAR = p.Suppress(')')

clumps = p.Forward()
brick = p.OneOrMore(p.oneOf('N W E S |')).setParseAction(
    lambda s, l, t: ''.join(t)
)
branch = LPAR + clumps + RPAR
branch.setParseAction(lambda s, l, t: [t])
clump = (brick | branch)
clumps << p.OneOrMore(clump)


def data():
    return open('20-input', 'r')


test_data = [
    "^WNE$",  # 3
    "^ENWWW(NEEE|SSE(EE|N))$",  # 10
    "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$",  # 18
    '^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$',  # 23
    '^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$'  # 31
]



# class Room:
#     def __init__(self, x, y, plan):
#         self.x = x
#         self.y = y
#         self.plan = plan
#         # NSEW.
#         self.walls = [None, None, None, None]


# class Map:
#     pass


# def dumbparse(data, state):
#     acc, stack = state

#     if data == []:
#         # err. stack? he empty?
#         return acc

#     ch = data.pop(0)

#     if ch == '(':
#         stack.append(acc)
#         return dumbparse(data, ([], stack))
#     if ch == ')':
#         if acc == []:
#             # we have a null step, I think.
#             acc = [None]
#         elif acc[-1] == []:
#             acc[-1] = None
#         return data, (stack.pop() + acc, stack)
#     if ch == '|':
#         return [acc] + dumbparse(data, [])
#     else:
#         acc.append(ch)
#         return dumbparse(data, (acc, stack))


# def dumbload(data):
#     return dumbparse(list(data)[1:-1], ([], []))

'ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))'
'ESSWWN(E|NNENN|(EESS|(WNSE)|SSS|WWWSSSSE|(SW|NNNE)))'
