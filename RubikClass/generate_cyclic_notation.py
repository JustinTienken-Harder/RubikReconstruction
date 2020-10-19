'''
Author: Justin Harder

Builds the cycles defined on all the stickers on a Rubik's cube from the common notation.
'''
from permutation_notation_parser import permutation_parser
from sticker_representation_cubie import Cubie
"""
String representation of the Rubik's cube is a 6*9 element array containing the following repeating colors (just the first lowercase letter is used in representation): White, Blue, Red, Green, Orange, Yellow

Each side has a number (0,1,2,3,4,5) respectively. This allows you to find whichever face as the orientation changes (U,B,R,F,L,D) respectively. The indices of each face is given by the following equation:

face_number*9 + sticker_location.

This allows us to easily calculate exact stickers based on the following sticker location chart:

                                0    1    2

                                3    4    5

                                6    7    8

Each "orientation" is determined by the shortest x/z rotation to get some face (say, 2) to the U layer. We adopt x2 as the rotation for getting the D layer to the U layer.
"""

#default = 'w'*9+'b'*9+"r"*9+"g"*9+'o'*9+'y'*9
'''
#OLD forgot when defining the corner cubie you need to go around it in one direction.
lookup = {"ULF":Cubie([6,4*9+8,3*9+0]),"ULB":Cubie([0,4*9+2,9+6]),
          "URF":Cubie([8,2*9+6,3*9+2]),"URB":Cubie([2,2*9+0,9+8]),
          "DLF":Cubie([5*9+0,4*9+6,3*9+6]),"DLB":Cubie([5*9+6,4*9+0,9+0]),
          "DRF":Cubie([5*9+2,2*9+8,3*9+8]),"DRB":Cubie([5*9+8,2*9+2,9+2]),
          "UR":Cubie([5,2*9+3]),"UL":Cubie([3,4*9+5]),
          "DR":Cubie([5*9+5,2*9+5]),"DL":Cubie([5*9+3,4*9+3]),
          "UF":Cubie([7,3*9+1]),"UB":Cubie([1,9+7]),
          "DF":Cubie([5*9+1,3*9+7]),"DB":Cubie([5*9+7,9+1]),
          "RF":Cubie([2*9+7,3*9+5]),"RB":Cubie([2*9+1,9+5]),
          "LF":Cubie([4*9+7,3*9+3]),"LB":Cubie([4*9+1,9+3])}
'''
def generate_moves():
    '''
    Returns two things: 
        1. The entire cyclic permutation where each index needs to be sent for all moves (RLUDFBMES), inverses, and half turns. 
        2. The lookup table (dict) for the indexes of a cubie in the 54-element list representation of a Rubik's Cube in terms of faces of cube.
    '''
    lookup_table = {"ULF":Cubie([6,4*9+8,3*9+0]),"ULB":Cubie([0,9+6,4*9+2]),
              "URF":Cubie([8,3*9+2,2*9+6]),"URB":Cubie([2,2*9+0,9+8]),
              "DLF":Cubie([5*9+0,3*9+6,4*9+6]),"DLB":Cubie([5*9+6,4*9+0,9+0]),
              "DRF":Cubie([5*9+2,2*9+8,3*9+8]),"DRB":Cubie([5*9+8,9+2,2*9+2,]),
              "UR":Cubie([5,2*9+3]),"UL":Cubie([3,4*9+5]),
              "DR":Cubie([5*9+5,2*9+5]),"DL":Cubie([5*9+3,4*9+3]),
              "UF":Cubie([7,3*9+1]),"UB":Cubie([1,9+7]),
              "DF":Cubie([5*9+1,3*9+7]),"DB":Cubie([5*9+7,9+1]),
              "RF":Cubie([2*9+7,3*9+5]),"RB":Cubie([2*9+1,9+5]),
              "LF":Cubie([4*9+7,3*9+3]),"LB":Cubie([4*9+1,9+3])}

    notation_corner = {"R":"URB -> BDR -> DRF -> FUR",
                        "U":"URB -> URF -> ULF -> ULB",
                        "L":"ULB -> FUL -> DLF -> BDL",
                        "D":"DRB -> DLB -> DLF -> DRF",
                        "F":"URF -> RDF -> DLF -> LUF",
                        "B":"URB -> LUB -> DLB -> RDB"}
    notation_edge = {"R":"UR -> BR -> DR -> FR",
                    "U":"UR -> UF -> UL -> UB",
                    "L":"UL -> FL -> DL -> BL",
                    "D":"DR -> DB -> DL -> DF",
                    "F":"UF -> RF -> DF -> LF",
                    "B":"UB -> LB -> DB -> RB",
                    "M":"UF -> FD -> DB -> BU",
                    "E":"RB -> BL -> LF -> FR",
                    "S":"UR -> RD -> DL -> LU"}
    center_cycle = {"M":(0*9+4, 3*9+4, 5*9+4, 1*9+4),
                    "E":(1*9+4, 4*9+4, 3*9+4, 2*9+4),
                    "S":(0*9+4, 2*9+4, 5*9+4, 4*9+4)}

    def expand_notation(dic):
        '''
        To convert all individual moves defined before to inverse and twice applied.
        '''
        for key, value in dic.copy().items():
            if type(value) is tuple:
                dic[key+"'"] = (value[0], value[3], value[2], value[1])
                dic[key+"2"] = [(value[0], value[2]),(value[1], value[3])]
            else:
                #Prime move
                prime_value = value.split(" -> ")
                prime_value[1], prime_value[3] = prime_value[3], prime_value[1]
                dic[key+"'"] = " -> ".join(prime_value)
                #2 move
                first = prime_value[0]+" -> "+prime_value[2]
                second = prime_value[1]+" -> "+prime_value[3]
                dic[key+"2"] = first + " & " + second

    #Convert our previously defined permutations into inverses and half-turns notation
    expand_notation(notation_corner)
    expand_notation(notation_edge)
    expand_notation(center_cycle)

    #these two lines feel like some cursed python. I'm sorry.
    #It converts a list [[1,2], [2,3]] to [1,2,2,3] when the first element is a list.
    #Otherwise it just returns the original list.
    #This is applied to values returned by permutation parser because
    #it sometimes returns lists of lists of tuples, and we just want a list of tuples
    flat_wrap = lambda func: lambda x: x if type(x[0]) is not list else func(x)
    flatten = flat_wrap(lambda l: [item for sublist in l for item in sublist])

    finalized_cycles = dict()
    for key, value in notation_edge.items():
        edge_cycle = flatten(permutation_parser(value, lookup_table))
        if key in notation_corner:
            corner_comm = notation_corner[key]
            corner_cycle = flatten(permutation_parser(corner_comm, lookup_table))
            edge_cycle.extend(corner_cycle)
        if key in center_cycle:
            x = flatten(center_cycle[key])
            if type(x) == list:
                edge_cycle.extend(x)
            else:
                edge_cycle.append(x)
        finalized_cycles[key] = edge_cycle
    return finalized_cycles, lookup_table


if __name__ == "__main__":
    tester = "URB -> DLF -> RBD"
    tester2 = 'RUB -> LFD -> DRB'
    