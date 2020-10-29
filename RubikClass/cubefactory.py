from groupcube import GroupCube
from sticker_cube import StickerCube


def decorate_cube_factory(func):
    '''Extends the functionality of cube factory so that we can change the default solve_state, but only once for consistency.'''
    def wrapper(cube_type = "string", new_solved_state = None, replace_solved_state = set()):
        """
        Function that produces cubes of various types depending on cube_type argument.

        Parameters:
            cube_type: "string" and "group" strings to return the respective representations of a Rubik's cube.

            new_solved_state: Replaces the cube_type's class attribute with this variable. Cannot replace twice.

            replace_solved_state: mutable object to keep track of classes with replaced solved_state
        """
        if cube_type in replace_solved_state:
            return func(cube_type)
        else:
            if new_solved_state is None:
                return func(cube_type)
            else:
                cube = func(cube_type)
                cube.__class__.solved_state = new_solved_state
                cube = func(cube_type) #have to get a new cube because class attribute is old.
                replace_solved_state.add(cube_type)
                return cube
    return wrapper

@decorate_cube_factory
def cube_factory(cube_type):
    if cube_type == "string":
        return StickerCube()
    elif cube_type == "group":
        return GroupCube()
    else:
        raise ValueError("Can only accept: string and group, and definitely not: " + str(cube_type))

        