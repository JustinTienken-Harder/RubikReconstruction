from Sticker_Permutation import permute_list_mutable #Used to turn cube
from generate_cyclic_notation import generate_moves
from permutation_notation_parser import permutation_parser
import pickle
from commutator_parser import parse_comm

class Cube: #Might actually be a representation of the abstract object.
    """
    Array representation of the Rubik's cube is a 6*9 element array containing the following repeating colors (just the first lowercase letter is used in representation): White, Blue, Red, Green, Orange, Yellow
    Each side has a number (0,1,2,3,4,5) respectively. This allows you to find whichever face as the orientation changes (U,B,R,F,L,D) respectively. 
    
    The indices of the sticker on every face is given by the following equation:

    face_number*9 + sticker_location.

    This allows us to easily calculate exact stickers based on the following sticker location chart:

                                    0    1    2

                                    3    4    5

                                    6    7    8

    Each "orientation" is determined by the shortest x/z rotation to get some face (say, R) to the U layer. We adopt x2 as the rotation for getting the D layer to the U layer.

    To represent the array as a more familiar representation. Holding a rubik's cube with white on U layer and green on F layer:

    Canonical Cube:
                            B-side
        *              |************|
        *              |*09**10**11*|
        *              |************|
        *              |*12**13**14*|
        *              |************|
        *              |*15**16**17*|
        *    L-side    |************|   R-side        
        * |************|************|************|
        * |*36**37**38*|*00**01**02*|*18**19**20*|
        * |************|************|************|
        * |*39**40**41*|*03**04**05*|*21**22**23*|
        * |************|************|************|
        * |*42**43**44*|*06**07**08*|*24**25**26*|
        * |************|************|************|
        *              |************|
        *              |*27**28**29*|
        *              |************|
        *              |*30**31**32*| F-side
        *              |************|
        *              |*33**34**35*|
        *              |************|
        *              |************|
        *              |*45**46**47*|
        *              |************|
        *              |*48**49**50*| D-side
        *              |************|
        *              |*51**52**53*|
        *              |************|
    """
    #A collection of turns that we commonly see that we remap to turns we can perform.
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
    #common mistakes are accidental pairs of moves, and some other things.
    _common_mistakes = pickle.load(open("common_mistakes.pckl", "rb"))
    #Both dictionaries. turn_to_cycle takes one of the 6*9 common moves and returns the cyclic permutation
    turn_to_cycle, cubie_lookup = generate_moves()
    solved_state = list('w'*9+'b'*9+"r"*9+"g"*9+'o'*9+'y'*9)

    def __init__(self):
        self.history = ""
        print(Cube.solved_state)
        #We could modify this for potentially learning to generate specific sub-steps, such as OLL/CMLL/etc
        self.current_state = Cube.solved_state.copy()
    
    def __call__(self, moves):
        '''
        --- Might want to inherit this from abstract Cube class ---
        '''
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
        out += "So far the moves performed are: " + str(self.history) + " \n"
        out += "The current state is given by: \n" 
        for i in range(6):
            out += str(self.current_state[i*9:(i+1)*9]) + "\n"
        return out

    def turn(self, letter):
        '''
        Applies a single turn to the Rubik's cube object. If the turn is unusual, it is remapped to turns we can do, and perform those.
        
        Moves all the stickers for a given turn.
        '''
        if letter in self._remap: #Can't do turn
            if type(self._remap[letter]) is list:
                for lett in self._remap[letter]:
                    self.turn(lett)
            else: #Must be a single remapped letter.
                self.turn(self._remap[letter])
        else: #Can do this turn.
            cycle = self.turn_to_cycle[letter]
            permute_list_mutable(self.current_state, cycle)
    
    #Would include basic_state_vector in here, but we already have the state represented as a vector.
    def string_parse(self,string):
        '''
        --- Might want to inherit this method from an abstract Cube Class --- 

        Method to parse input strings. Replaces anything with parenthesis, commas, newlines, forward or backslashes with spaces. 
        Removes any illegible turns which might be comments or empty strings.
        Can also handle simple commutators.

        Returns a list of turns.


        Todo:

        - Parse strings without spaces between turns.
        - Expand inverse of a set of moves in the parse_commutator call

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
    
    def reset(self):
        self.history = ""
        self.current_state = Cube.solved_state.copy()

    def is_solved(self):
        '''
        Method to check if the cube is "solved". 
        
        Slow method is implemented if we ever want to redefine what a "solved" state to allow for blacked out stickers (such as CMLL).

        Fast method checks the number of distinct colors on each side. 
        Slow method performs all 24 rotations to the cube. Only occurs if you redefine Cube class's global solved_state.
        '''
        #This is the boolean value that checks if we modified the Cube class from some other file. If this is the case we use the slow version.
        slow = Cube.solved_state != list('w'*9+'b'*9+"r"*9+"g"*9+'o'*9+'y'*9)
        print(slow, " slow")
        print("SOLVED STATE:", Cube.solved_state)
        if slow:
            #We just generate each rotation. Make another cube object in the solved state, and rotate the solved cube until it matches with unsolved cube
            first_rotation = {'','x', 'x2', "x'", 'z', "z'"}
            second_rotation = {"","y", "y'", "y2"}
            all_rotations = [x+y for x in first_rotation for y in second_rotation]
            comparison_cube = Cube()
            for rotation in all_rotations:
                comparison_cube(rotation)
                if comparison_cube.current_state == self.current_state:
                    return True
                comparison_cube.reset()
            return False
        else:
            set_of_sticker_colors_per_side = [set(self.current_state[i*9:(i+1)*9]) for i in range(6)]
            distinct_stickers_per_side = [len(x) for x in set_of_sticker_colors_per_side]
            print(distinct_stickers_per_side)
            if sum(distinct_stickers_per_side) == 6: #Each side has only one distinct color
                return True
            else:
                return False



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
    print(rubik)
    print("Is the cube solved? " + str(rubik.is_solved()))
    rubik(bad_comm)
    print(rubik)
    print("Is the cube solved? " +str(rubik.is_solved()))
    import sys
    sus_string = " ".join(sys.argv[1:])
    rubik(sus_string)
    print(rubik)
