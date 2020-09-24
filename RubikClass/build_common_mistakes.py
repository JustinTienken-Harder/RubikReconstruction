blah = {  'x': ['R', "M'", "L'"], 'x2': ['R2', 'M2', 'L2'], "x'": ["R'", 'M', 'L'], 'y': ['U', "E'", "D'"],
                'y2': ['U2', 'E2', 'D2'], "y'": ["U'", 'E', 'D'], 'z': ['F', 'S', "B'"], 'z2': ['F2', 'S2', 'B2'],
                "z'": ["F'", "S'", 'B'], 'r': ['R', "M'"], 'r2': ['R2', 'M2'], "r'": ["R'", 'M'], 'l': ['L', 'M'],
                'l2': ['L2', 'M2'], "l'": ["L'", "M'"], 'f': ['F', 'S'], 'f2': ['F2', 'S2'], "f'": ["F'", "S'"],
                'b': ['B', "S'"], 'b2': ['B2', 'S2'], "b'": ["B'", 'S'], 'u': ['U', "E'"], 'u2': ['U2', 'E2'],
                "u'": ["U'", 'E'], 'd': ['D', 'E'], 'd2': ['D2', 'E2'], "d'": ["D'", "E'"],
                'Rw': 'r', 'Rw2': 'r2', "Rw'": "r'", 'Lw': 'l', 'Lw2': 'l2', "Lw'": "l'", 'Fw': 'f', 'Fw2': 'f2',
                "Fw'": "f'", 'Bw': 'b', 'Bw2': 'b2', "Bw'": "b'", 'Uw': 'u', 'Uw2': 'u2', "Uw'": "u'", 'Dw': 'd',
                'Dw2': 'd2', "Dw'": "d'", "u3'": 'u', 'l3': "l'", "r2'": 'r2', "b2'": 'b2', "S3'": 'S', 'x3': "x'",
                "b3'": 'b', "Lw2'": 'Lw2', 'Lw3': "Lw'", "y3'": 'y', "M2'": 'M2', "z2'": 'z2', 'L3': "L'", 'Uw3': "Uw'",
                "z3'": 'z', "F3'": 'F', "R3'": 'R', "y2'": 'y2', 'b3': "b'", "d2'": 'd2', "L2'": 'L2', 'f3': "f'", "Uw2'": 'Uw2',
                "B3'": 'B', 'd3': "d'", "d3'": 'd', "M3'": 'M', "D2'": 'D2', "Lw3'": 'Lw', "Rw3'": 'Rw', 'U3': "U'", "l2'": 'l2',
                "Fw3'": 'Fw', 'Dw3': "Dw'", "x3'": 'x', "S2'": 'S2', "D3'": 'D', 'S3': "S'", "L3'": 'L', "f2'": 'f2', "Rw2'": 'Rw2',
                "r3'": 'r', "R2'": 'R2', 'r3': "r'", 'Rw3': "Rw'", 'F3': "F'", 'u3': "u'", "Dw2'": 'Dw2', "U2'": 'U2', 'z3': "z'",
                "l3'": 'l', "f3'": 'f', "U3'": 'U', 'Bw3': "Bw'", "Bw3'": 'Bw', 'R3': "R'", "E2'": 'E2', "u2'": 'u2', "Bw2'": 'Bw2',
                'B3': "B'", 'y3': "y'", 'Fw3': "Fw'", "Fw2'": 'Fw2', 'E3': "E'", "x2'": 'x2', "Dw3'": 'Dw', 'D3': "D'", 'M3': "M'",
                "E3'": 'E', "Uw3'": 'Uw', "B2'": 'B2', "F2'": 'F2'}

legal = {'M', 'Dw', 'u', 'R2', 'r2', 'y2', "E'", "x'", 'd2', 'B2', 'E2', 'y', 'L2', 'z',
                 'S2', "r'", 'F2', 'x2', 'Bw2', 'b', 'M2', "B'", 'Uw', 'D2', "Fw'", 'r', "Lw'",
                 'S', 'Rw2', 'L', "L'", "Rw'", 'F', "F'", "D'", 'Fw', "U'", 'U2', "u'", "f'", 'Rw',
                 'f', 'b2', 'D', 'x', 'Lw', 'Lw2', 'E', 'f2', 'u2', 'l', "R'", "l'", 'Uw2', "d'", 'Bw',
                 'R', "z'", 'Dw2', "Uw'", "b'", "Dw'", "S'", 'l2', "y'", 'z2', "M'", 'Fw2', 'd', "Bw'", 'B', 'U'}

legal = legal.union(set(blah.keys()))

common_mistakes = dict()
for x in legal:
  for y in legal:
    common_mistakes[x+y] = x+" "+y

#print(common_mistakes)

import pickle
with open("common_mistakes.pckl", "wb") as f:
  pickle.dump(common_mistakes, f)

x = pickle.load(open("common_mistakes.pckl", "rb"))
print(x)
