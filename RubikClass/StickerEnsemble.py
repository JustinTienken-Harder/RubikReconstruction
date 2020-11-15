from abstract_cube import AbstractCube

from cubefactory import cube_factory

import numpy as np
import random


class EnsembleStickerCube(AbstractCube):
    """
    Object to directly interact with an entire collection of rubik's cubes at the same time.

    By default constructs all 24 orientations of a rubik's cube!
    Has option for only 2 cubes, and apply a move only to one cube.
    """
    orientations = [None, "x", "x2", "x'", "z", "x y", "z' y2", "z x'", "z2", "x y2", "y2", "x' y2",
             "z'", "z' x", "z y2","z' x'", "y", "x z'", "y' z2", "z y", "z' y'", "y'", "z y'", "z' y"]
    def __init__(self, default = True, randomize_representation = False):
        self.default = default
        self.random = randomize_representation
        if default:
            self.cubes = [cube_factory("string") for x in range(24)]
            self._reorient_all()
        else:
            self.cubes = [cubefactory("string") for x in range(2)]

    def __str__(self):
        out = "".join([cube.__str__() for cube in self.cubes])
        return out

    @AbstractCube.recursively_remap
    def turn(self, letter):
        """Applies turn to every cube object"""
        for cube in self.cubes:
            cube.turn(letter)

    def reset(self):
        for cube in self.cubes:
            cube.reset()
        if self.default:
            self._reorient_all()

    def is_solved(self):
        for cube in self.cubes:
            solved = cube.is_solved()
            break
        return solved

    def _reorient_all(self):
        """Reorients all 24 cubes, generally called after initialization or resetting the cube."""
        if not self.default:
            raise("This only works for default 24 cube ensemble")
        for i in range(24):
            if i == 0:
                pass
            else:
                rotation = EnsembleStickerCube.orientations[i]
                self.cubes[i](rotation)

    def visualize(self):
        """
        For default arguments, provides a 36*36 pixel image of all the cubes visualized into an array of shape (36, 36, 3)

        no implementation for non-default arguments.
        """
        if self.random:
            self.cubes = random.sample(self.cubes, len(self.cubes))
        sticker_arrays = [cube.visualize() for cube in self.cubes]
        if self.default:
            temporary = []
            for i in range(4):
                temporary.append( np.concatenate(sticker_arrays[(i*6):((i+1)*6)]) )
            out = np.hstack(temporary)
            return out
        else:
            return np.concatenate(sticker_arrays)
