import pickle
from commutator_parser import parse_comm

def permute(d, p):
    '''
    Takes a dictionary of the current cubie permutations, and then applies the cycle notation permutation to it.

    For example, if we have the identity cubie permutation: {0:0, 1:1, 2:2, 3:3}
    And we wish to apply the following cycle notation permutation to it: [0,1,2,3]

    The result is {0:3, 1:0, 2:1, 3:2} with interpretation as, the 0 position currently contains the 3rd cubie.
    The cycles are interpreted as: The cubie in the 0 position goes to the 1th position (and the cubie in the 1st position goes to the 3rd position, etc).
    '''
    def _permute(d, p):
        '''
        Helper function to apply only one cyclic permutation.
        '''
        #Consider the following running example for p = [4,5,6,7]
        #use this for modular arithmetic to get the element before the current element
        mod = len(p)
        #the 0th element of the cycle (4) will have the dictionary value associated with the -1th element of the cycle (7), essentially doing dictionary[4] = dictionary[7]
        # across all elements of the array, but without any conflicts associated with doing it in a loop (because we have a cyclic permutation)
        # This operation makes a new temporary dictionary, so we don't accidentally get duplicate elements
        temp = dict((p[x], d[p[(x-1) % mod]]) for x, y in enumerate(p))
        #Because we moved the values associated with 4,5,6,7 in a cycle, we now want to "append" the dictionary values we did not touch.
        out = dict((x,temp[x]) if x in temp else (x,y) for x,y in d.items())
        return out
    #Apply permute
    if p is None:
        return d
    if type(p[0]) is list:
        for perm in p:
            d = _permute(d, perm)
    else:
        d = _permute(d, p)
    return d


class Cube:
    '''
    The Rubik's Cube class. Contains the appropriate information to represent and perform turns on a representation of a rubik's cube.

    The most important method to interact with the cube is actually the call, i.g.,
    rubik = Cube()
    rubik("R U R' U'")


    Edge and Corner orientation follows an absolute orientation that follows the cubies (i.e., implemented as the wreath product of the cubie permutations)

    The corner/edge permutations are implemented as dictionaries whose keys are the locations relative to the cannonical cube, and the values are the cubies located in that position.
    For example, an R move will send C1->C5->C6->C2->C1 and change C1's orientation by +1, but C2's by +2, etc.
    From solved, the resulting permutation will be: {1:2, 5:1, 6:2, 2:6, i:i}. Permutations work in a manner such that whatever cubie number is currently in position 1 will be sent to position 5.
    For edges, we get 1->5->9->6->1 with no edge orientation changes.
    The centers are also labeled, but with the respective face of the cube if you were holding it. Changing orientation is equivalent to turning all three layers.

    The following diagram has C1 to denote that self._corner_perm[0] = 0 is that location, E1 is the edge denoted with 1 in edge permutation.

    Canonical Cube:
                          U layer
         *              |************|
         *              |*C0**E0**C1*|
         *              |************|
         *              |*E3**U0**E1*|
         *              |************|
         *              |*C3**E2**C2*|
         *              |************|
         * |************|************|************|************|
         * |*C0**E3**C3*|*C3**E2**C2*|*C2**E1**C1*|*C1**E0**C0*|
         * |************|************|************|************|
         * |*E4**L4**E7*|*E7**F3**E6*|*E6**R2**E5*|*E5**B1**E4*|
         * |************|************|************|************|
         * |*C4**11**C7*|*C7**10**C6*|*C6**E9**C5*|*C5**E8**C4*|
         * |************|************|************|************|
         *              |************|
         *              |*C7**10**C6*|
         *              |************|
         *              |*11**D5**E9*|
         *              |************|
         *              |*C4**E8**C5*|
         *              |************|

         Todo:
         - Implement a method to check if the cube is solved. Presumably by making a copy of the permutations,
            then reorienting the cube to the standard orientation (apply rotations to copy so that centers is back to 0:0, 1:1).
            Finally check to see if edges/corner orientation/permutation are the defaults.
         - Do some more rigorous unit testing, and do more input checking
         - Upgrade string_parse to accept strings without spaces such as "RUR'U'"
    '''
    # Static variable defining how to remap some moves into a sequence of other moves
    _remap = {  'x': ['R', "M'", "L'"], 'x2': ['R2', 'M2', 'L2'], "x'": ["R'", 'M', 'L'], 'y': ['U', "E'", "D'"],
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

    #Static variable defining the permute corners operation for cube notation
    _mco  = {  "U": [0,1,2,3], "U2": [[0,2],[1,3]], "U'": [0,3,2,1],
                    "R": [2,1,5,6], "R2": [[2,5],[1,6]], "R'": [2,6,5,1],
                    "L": [0,3,7,4], "L2": [[0,7],[4,3]], "L'": [0,4,7,3],
                    "F": [3,2,6,7], "F2": [[3,6],[2,7]], "F'": [3,7,6,2],
                    "B": [1,0,4,5], "B2": [[1,4],[0,5]], "B'": [1,5,4,0],
                    "D": [7,6,5,4], "D2": [[7,5],[6,4]], "D'": [7,4,5,6]}

    #Static variable defining the permute edges operation for cube notation
    _me = {    "U": [0,1,2,3], "U2": [[0,2],[3,1]], "U'": [0,3,2,1],
                    "R": [1,5,9,6], "R2": [[1,9],[5,6]], "R'": [1,6,9,5],
                    "L": [3,7,11,4],"L2": [[3,11],[7,4]],"L'": [3,4,11,7],
                    "F": [2,6,10,7],"F2": [[2,10],[6,7]],"F'": [2,7,10,6],
                    "B": [0,4,8,5], "B2": [[0,8],[4,5]], "B'": [0,5,8,4],
                    "D": [10,9,8,11],"D2": [[10,8],[9,11]],"D'": [10,11,8,9],
                    "M": [0,2,10,8],"M2": [[0,10],[2,8]],"M'": [0,8,10,2],
                    "E": [7,6,5,4], "E2": [[7,5],[6,4]], "E'": [7,4,5,6],
                    "S": [3,1,9,11],"S2": [[3,9],[1,11]],"S'": [3,11,9,1]}

    #Static variable defining how to orient corners after a move
    _oc = {"R": {1:1, 5:2, 6:1, 2:2}, "R'": {1:1, 5:2, 6:1, 2:2},
                "L": {0:2, 3:1, 7:2, 4:1}, "L'": {0:2, 3:1, 7:2, 4:1},
                "F": {2:1, 6:2, 7:1 , 3:2}, "F'": {2:1, 6:2, 7:1, 3:2},
                "B": {0:1, 1:2, 4:2 , 5:1}, "B'": {0:1, 1:2, 4:2 , 5:1}}

    #Static variable defining how to permute centers after a move.
    _mce = {"M":[0,3,5,1], "M2":[[0,5],[3,1]], "M'":[0,1,5,3],
                 "E":[1,4,3,2], "E2":[[1,3],[4,2]], "E'":[1,2,3,4],
                 "S":[0,2,5,4], "S2":[[0,5],[2,4]], "S'":[0,4,5,2]}

    #Load up common mistakes
    _common_mistakes = pickle.load(open("common_mistakes.pckl", "rb"))

    def __init__(self):
        '''
        Setting up the underlying data for a cube's representation
        '''
        self.history = ""
        self._corner_perm = dict((x,x) for x in range(8))
        self._edge_perm = dict((x,x) for x in range(12))
        self._corner_orient = dict((x,0) for x in range(8))
        self._edge_orient = dict((x,0) for x in range(12))
        self._center = dict((x,x) for x in range(6))

    def __call__(self, moves):
        if type(moves) is list:
            self.history += " "+" ".join(moves)
            for move in moves:
                self.turn(move)
        elif type(moves) is str:
            moves = self.string_parse(moves)
            self.history += " "+" ".join(moves)
            for move in moves:
                self.turn(move)
        else:
            print("This can only accept lists of turns, or strings that can be appropriately parsed")

    def __str__(self):
        out = ""
        out += "So far the moves performed are:"+ str(self.history) + " \n"
        out += "The current state of corners are: " + str(self._corner_perm) + " \n"
        out += "The current corner's orientation: " + str(self._corner_orient) + " \n"
        out += "The current state of edges are: "+ str(self._edge_perm) + " \n"
        out += "The current edge's orientation: " + str(self._edge_orient) + " \n"
        out += "The current cube orientation is: " + str(self._center) + " \n"
        return out

    def turn(self, letter):
        '''
        Applies a single turn to the rubik's cube object. If the turn is unusual (such as a rotation or Rw), it first remaps the turn to it's associated subturns, then performs those subturns. It's done in the following order:

        Permute corners, reorient corners, permute edges, reorient edges, permute centers
        '''
        if letter in Cube._remap:
            if type(Cube._remap[letter]) is list:
                for lett in Cube._remap[letter]:
                    self.turn(lett)
            else: #Must be a single remapped letter.
                self.turn(Cube._remap[letter])
        else:
            if letter in Cube._mco:
                self._corner_perm = permute(self._corner_perm, Cube._mco[letter]) #Permute corners according to the cycle in lookup table
            if letter in Cube._oc: #otherwise the was no corner orientation change
                for position, twist in Cube._oc[letter].items(): #for each position effected by turn
                    cil = self._corner_perm[position]            #get the cubie now located in the new position
                    self._corner_orient[cil] = (self._corner_orient[cil] + twist) % 3 #Twist the cubie's absolute orientation
            if letter in Cube._me:
                self._edge_perm = permute(self._edge_perm, Cube._me[letter]) #Permute edges according to cycle in lookup table
            if letter in {"F", "F'", "B", "B'","M", "M'", "S", "S'", "E", "E'"}: #Then the turn effects edge orientation
                reorient = [self._edge_perm[x] for x in Cube._me[letter]] #get the cubies now located in the new position
                for cubie in reorient:
                    self._edge_orient[cubie] = (self._edge_orient[cubie] + 1) % 2 #flip the edges over
            if letter in Cube._mce:
                self._center = permute(self._center, Cube._mce[letter])

    def basic_state_vector(self):
        '''
        Method to return the current state of the cube as a vector of numbers (useful for training a Neural Network):

        Looks like:
        [corner_orient, corner_permute, edge_orient, edge_permute]
        For a solved cube:
        [0,0,0,0,0,0,0,0,
         0,1,2,3,4,5,6,7,    0,0,0,0,0,0,0,0,0,0,0,0,
                             0,1,2,3,4,5,6,7,8,9,10,11]

        Only good for finding solutions that doesn't utilize moves that change the cube's orientation (both for computation speed, and ease of implementation)
            Todo:
                - Create a better, more versatile representation that is either lower-dimensional or allows for changing cube orientations
        '''
        out= []
        out.extend(self._corner_orient[x] for x in range(8))
        out.extend(self._corner_perm[x] for x in range(8))
        out.extend(self._edge_orient[x] for x in range(12))
        out.extend(self._edge_perm[x] for x in range(12))
        return out

    def string_parse(self, string):
        '''
        Method to parse input strings. Replaces anything with parenthesis, commas, newlines, forward or backslashes with spaces. Removes any illegible turns which would be comments or empty strings.

        Returns a list of turns.


        Todo:

        - Add Commutator notation functionality for parsing (conjugates and commutators).

        - Parse strings without spaces between turns.

        '''
        #replace common things we'll find with spaces
        replacements = [("\n"," "), ("("," "), (")"," "), ("/"," "), ("\\", " "), ("["," [ "), ("]"," ] "), (","," , "), (":"," : ")]
        for item, replacement in replacements:
            string = string.replace(item, replacement)
        moves = string.split(" ")
        legal = {",", ":", "[", "]",
                'M2', 'U2', 'b2', 'L2', "y3'", 'D', "Lw3'", 'Bw2', 'x', 'F2', "M3'", 'l', 'b3', 'r3', 'f2', "Uw2'", 'R', 'd',
                "D'", 'Fw', 'D3', "F2'", "D3'", "b3'", 'U3', 'Dw3', "r2'", 'L3', "Dw2'", "l3'", 'E3', "l'", "Rw3'", "Rw'", "Dw'",
                "Bw3'", "M2'", "D2'", "Uw'", "S'", 'S', "z3'", 'M', 'Lw2', "u3'", "F'", "r3'", 'u2', "Fw3'", 'Uw3', 'l3', "x3'",
                'r2', 'f3', "L'", 'y', 'U', "Fw'", 'F', 'd2', 'Uw', 'l2', 'u3', "R3'", "d3'", "d2'", "R'", "L3'", "Bw'", "r'", "f3'",
                "S2'", "x'", "E2'", "d'", 'Bw', "u'", 'S3', "Bw2'", "E'", 'x3', 'R3', 'R2', "M'", "U3'", "B2'", "U'", "Fw2'", 'x2',
                "l2'", 'y3', 'S2', "u2'", 'b', 'u', 'd3', "Dw3'", 'z3', 'B2', 'y2', "Uw3'", "B3'", "R2'", "Lw'", 'E2', "b2'", 'F3',
                'Lw3', 'Lw', "y'", 'Fw2', 'Dw2', "f2'", "L2'", 'L', "x2'", 'z', 'B', 'M3', "B'", 'E', 'Dw', "z'", "F3'", 'Rw3', "S3'",
                "Rw2'", 'D2', 'Bw3', "f'", 'z2', "b'", 'B3', "z2'", "U2'", 'Rw2', "Lw2'", 'Uw2', 'f', 'Fw3', "y2'", 'Rw', 'r', "E3'"}
        #replace all common spacing mistakes in the list
        moves = [Cube._common_mistakes[x] if x in Cube._common_mistakes else x for x in moves]
        moves = " ".join(moves).split(" ") #combine and then split it on space to remove any illegal moves
        legal_moves = [x for x in moves if x in legal]
        commutator_remains = " ".join(legal_moves) #make a string for parse_comm
        #Hopefully nobody uses stuff like Rw in a commutator, otherwise we'll need to update the inverse function
        #We will find out when we test out the database.
        last_cleaning = parse_comm(commutator_remains)
        #This will remove any duplicate spaces introduced by parsing the commutator
        out = [x for x in last_cleaning.split(" ") if x != ""]
        #join on spaces and pass it off
        return out

    def is_solved(self):
        '''
        Method to check if the current state of the cube is solved.

        Achieved by making a new cube class instance, reorients unscrambled cube to match the current cube, then compares current cube's permutation to the solved cube.
        '''
        def compare_cubes(a, b):
            """
            Compares two cube classes to make sure that they both have equivalent permutations and orientations
            """
            if a._center != b._center:
                print("We aren't even oriented properly in compare_cubes(a,b)!")
                return False
            if a._corner_perm == b._corner_perm and (a._corner_orient == b._corner_orient) and (a._edge_perm == b._edge_perm) and (a._edge_orient == b._edge_orient):
                return True
            else:
                return False
        solved_cube = Cube()
        #Look at the center currently in self._center[0]. Then do the rotation on the solved cube so the centers line up.
        first_rotation = {0:None, 1:"x'", 2:"z'", 3:"x", 4:"z", 5:"x2"}
        rotation_one = first_rotation[self._center[0]]
        if rotation_one is not None:
            solved_cube.turn(rotation_one)
        #Given that the 0 side of solved cube is where it needs to be:
        #Define rotations to send side x to side 3
        second_rotation = {1:"y2", 2:"y", 3:None, 4:"y'"}
        #Make a table to lookup where a center is currently located
        find_location_of_solved_centers = dict((y,x) for x,y in solved_cube._center.items())
        #Find what cubie is currently in the 3 center for the unsolved cube
        center_cubie_of_unsolved_cube = self._center[3] #such as 2
        #Using the previous cubie number, locate where this cubie's "absolute" location on the solved cube.
        #because the U side is correctly oriented, it must be 1, 2, 3, 4
        side_to_send_to_three = find_location_of_solved_centers[center_cubie_of_unsolved_cube]
        rotation_two = second_rotation[side_to_send_to_three]
        if rotation_two is not None:
            solved_cube.turn(rotation_two)
        #Finally, check that the two cubes are solved
        return compare_cubes(self, solved_cube)

if __name__  == "__main__":
    scramble = "L2 B D B' R' L' U F L' U' R2 U B2 L2 D2 B2 R2 U2 F2 U B2"
    solution = """x' z2 f U' S U' S'
R' U2' R' U2 R U' R'
U' R' U' R U R' U2' R
U2 F R U R' U' R U R' U' F'
U2 M U' U2' M U'M' U2' M' U2' M2'"""
    bad_comm = "[["+scramble+":[[R,U],[R,U]]]:[R2 F2 U2: R2] [U': [F2,U2] F2]]"
    rubik = Cube()
    rubik(scramble)
    print(rubik)
    rubik(solution)
    print("So far the moves performed are: "+ rubik.history)
    print("Is the cube solved? " + str(rubik.is_solved()))
    rubik(bad_comm)
    print(rubik)
    print("Is the cube solved? " +str(rubik.is_solved()))
    import sys
    sus_string = " ".join(sys.argv[1:])
    rubik(sus_string)
    print(rubik)
