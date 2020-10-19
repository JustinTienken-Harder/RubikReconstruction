class Cubie(list):
    def __init__(self,input_list):
        '''
        Essentially defines the index locations of each element of a cubie inside of the string. Will allow for easier manipulations of the cube depending on the moves performed.

        Representation of a cubie follows this formal schema of index locations referenced by order of importance:

        [U/D, R/L, F/B]

        The first element of a cubie should be the face with most priority, subsequent elements are faces counterclockwise from that inital face:

        This means for an edge, it's sticker locations (in the list representation) will always be ordered by the aforementioned order of importance.

        The __call__ method allows us to rotate pieces's absolute canonical order. Useful for parsing cuber permutation notation.
        '''
        self.default_value = list(input_list)
        if len(input_list) == 3:
            self.type = "c"
        elif len(input_list) == 2:
            self.type = "e"
        else:
            ValueError("Cannot input a list of sizes other than 2 or 3.")

    def __call__(self, twist_or_flip_str = "i"):
        '''
        twist_or_flip_str: Can take values and interpretations as
        "i": identity
        "f": flip the edge, error on corner
        1: clockwise twist (or flip edge)
        2: 2 clockwise twists (or identity on edge)
        -1: counterclockwise twist (or flip edge)
        -2: two counterclockwise twists (or identity on edge)
        0: identity
        "+": Clockwise twist (or flip edge)
        "-": Counterclockwise twist (or flip edge)
        '''
        t = twist_or_flip_str
        if self.type == "e":
            if t in {"i", 2, "2", -2, "-2", 0, "0"}:
                return self.default_value
            elif t in {"f", "+", "-1", "1", "-", 1, -1}:
                edge = self.default_value #we have to mutate edge
                out = [None, None]
                out[0], out[1] = edge[1], edge[0]
                return out
            else:
                raise AttributeError("Cannot accept argument" + str(t))
        else: #must be a Corner
            if t in {"i", "0", 0}:
                return self.default_value
            c = self.default_value
            if t in {"1", 1, "+", -2, "-2"}:
                o = [None, None, None]
                o[0], o[1], o[2] = c[2], c[0], c[1]
                return o
            elif t in {"-1", -1, 2, "2", "-"}:
                o = [None, None, None]
                o[0], o[1], o[2] = c[1], c[2], c[0]
                return o
            else:
                raise AttributeError("Cannot accept argument" + str(t))


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

#default_cube_string = 'w'*9+'b'*9+"r"*9+"g"*9+'o'*9+'y'*9
