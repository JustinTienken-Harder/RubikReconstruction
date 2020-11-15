#base
from functools import wraps
import pickle

#custom
from commutator_parser import parse_comm

#factory
#interfaces -- implements
#patterns
#extending class -- also known as composition
#singleton
#abstract method in python
#dependency inversion principle

def make_turn_recursively_remap(turn_method):
    @wraps(turn_method)
    def wrapper(obj, letter, *args, **kwargs):
        if letter in AbstractCube._remap:
            if isinstance(AbstractCube._remap[letter], (list, tuple)):
                for lett in AbstractCube._remap[letter]:
                    wrapper(obj, lett, *args, **kwargs)
            else: #Must be a single remapped letter.
                wrapper(obj, AbstractCube._remap[letter], *args, **kwargs)
        else: #no need for remapping.
            turn_method(obj, letter, *args, **kwargs)
    return wrapper


common_mistakes = pickle.load(open("common_mistakes.pckl", "rb"))

class AbstractCube:
    """Abstract Rubik's Cube class. All other representations of a Rubik's cube will inheret from this class.


    Every representation of a Cube will have the following default methods and attributes:

        _remap: Collection of moves that are commonly seen but are implemented through other turns

        recursively_remap: A function that can be used to wrap any subclass's turn method to recursively remap moves if they aren't implemented.

        string_parse: function to parse a string into a list of moves -- replaces common mistakes and parses commutator notation.

        _common_mistakes: Dictionary of common mistakes in notation that we'll replace.

        __call__(): accepts lists of turns or strings of moves. Performs these moves on the current cube. No return.

        history: string to keep track of the cube's history.


    Every cube representation must implement these methods:

        turn():


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
    _common_mistakes = common_mistakes
    history = ""

    #Put all methods that are common between every cube. Commutator Parser, string parser, etc.
    def __call__(self, moves):
        if isinstance(moves, (list, tuple)):
            self.history += " "+" ".join(moves)
            for move in moves:
                self.turn(move)
        elif isinstance(moves, str):
            moves = self.string_parse(moves)
            self.history += " "+" ".join(moves)
            for move in moves:
                self.turn(move)
        else:
            print("This can only accept lists of turns, or strings that can be appropriately parsed")

    def string_parse(self, string):
        '''
        Method to parse input strings. Replaces anything with parenthesis, commas, newlines, forward or backslashes with spaces. Removes any illegible turns which would be comments or empty strings.

        Returns a list of turns.


        Todo:

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
        moves = [AbstractCube._common_mistakes[x] if x in AbstractCube._common_mistakes else x for x in moves]
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
        """Must implement a reset method on any representation."""
        raise NotImplementedError(AbstractCube.reset.__doc__)

    #Functions that allows child class to decorate a basic turn so that it'll recursively remap unperformable turns
    recursively_remap = lambda func: make_turn_recursively_remap(func)
    def turn(self, move):
        """
        Every Representation (or child) of an AbstractCube must implement a turn method.

        Minimally, you must be able to perform the following moves:
                    "U", "U2", "U'",
                    "R", "R2", "R'",
                    "L", "L2", "L'",
                    "F", "F2", "F'",
                    "B", "B2", "B'",
                    "D", "D2", "D'",
                    "M", "M2", "M'",
                    "E", "E2", "E'",
                    "S", "S2", "S'"

        Handling all other moves is done automatically if the __init__ method of Representation has the line: super(Representation, self).__init__()
        """
        #Raises the docstring as a not-implemented error
        raise NotImplementedError(AbstractCube.turn.__doc__)


    def is_solved(self):
        """Must provide a method to check if a particular representation is solved. Should return True or False."""
        raise NotImplementedError(AbstractCube.is_solved.__doc__)

    def current_state(self):
        """Must implement a current state field within any representation of a Rubik's Cube"""
        raise NotImplementedError(AbstractCube.current_state.__doc__)

    def solved_state(self):
        """Must implement a solved state field within any representation of a Rubik's Cube"""
        raise NotImplementedError(AbstractCube.solved_state.__doc__)
