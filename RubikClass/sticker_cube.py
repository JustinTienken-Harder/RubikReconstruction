from cyclic_permutation import permute_list_mutable #Used to turn cube
from generate_cyclic_notation import generate_moves
from visualize_stickered_cube import pixel_value_sticker

from abstract_cube import AbstractCube

class StickerCube(AbstractCube): #Might actually be a representation of the abstract object.
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
    #Both dictionaries. turn_to_cycle takes one of the 6*9 common moves and returns the cyclic permutation
    turn_to_cycle, cubie_lookup = generate_moves()
    solved_state = list('w'*9+'b'*9+"r"*9+"g"*9+'o'*9+'y'*9)

    def __init__(self):
        self.history = ""
        #We could modify this for potentially learning to generate specific sub-steps, such as OLL/CMLL/etc
        self.current_state = StickerCube.solved_state.copy()

    def __str__(self):
        out = ""
        out += "So far the moves performed are: " + str(self.history) + " \n"
        out += "The current state is given by: \n"
        for i in range(6):
            out += str(self.current_state[i*9:(i+1)*9]) + "\n"
        return out

    @AbstractCube.recursively_remap
    def turn(self, letter):
        '''
        Applies a single turn to the Rubik's cube object.

        Moves all the stickers for a given turn.
        '''
        cycle = self.turn_to_cycle[letter]
        permute_list_mutable(self.current_state, cycle)

    #Would include basic_state_vector in here, but we already have the state represented as a vector.
    def reset(self):
        self.history = ""
        self.current_state = StickerCube.solved_state.copy()

    def visualize(self, compact = True, color =True):
        """
        Returns an array of the current state of the cube. Must convert to numpy array for most purposes!

        Colors are hard-coded;
        Acceptable stickers are 'w','b','r','g','o','y','e','';
        Two representations, colorful (3 channel) or black and white (1 channel);
        Shape is (6, 9, 3) if color, else (6, 9)
        """
        image_numpy_array = pixel_value_sticker(sticker_array = self.current_state, bandw = True)
        return image_numpy_array

    def is_solved(self):
        '''
        Method to check if the cube is "solved".

        Slow method is implemented if we ever want to redefine what a "solved" state to allow for blacked out stickers (such as CMLL).

        Fast method checks the number of distinct colors on each side.
        Slow method performs all 24 rotations to the cube. Only occurs if you redefine Cube class's global solved_state.
        '''
        #This is the boolean value that checks if we modified the Cube class from some other file. If this is the case we use the slow version.
        slow = StickerCube.solved_state != list('w'*9+'b'*9+"r"*9+"g"*9+'o'*9+'y'*9)
        #print(slow, " slow")
        #print("SOLVED STATE:", StickerCube.solved_state)
        if slow:
            #We just generate each rotation. Make another cube object in the solved state, and rotate the solved cube until it matches with unsolved cube
            first_rotation = {'','x', 'x2', "x'", 'z', "z'"}
            second_rotation = {"","y", "y'", "y2"}
            all_rotations = [x+y for x in first_rotation for y in second_rotation]
            comparison_cube = StickerCube()
            for rotation in all_rotations:
                comparison_cube(rotation)
                if comparison_cube.current_state == self.current_state:
                    return True
                comparison_cube.reset()
            return False
        else:
            set_of_sticker_colors_per_side = [set(self.current_state[i*9:(i+1)*9]) for i in range(6)]
            distinct_stickers_per_side = [len(x) for x in set_of_sticker_colors_per_side]
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
    rubik = StickerCube()
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
