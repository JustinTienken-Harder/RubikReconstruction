def permute(d, p):
    '''
    Takes a dictionary of the current cubie permutations, and then applies the cycle notation permutation to it.

    For example, if we have the identity cubie permutation: {0:0, 1:1, 2:2, 3:3}
    And we wish to apply the following cycle notation permutation to it: [[0,2], [1,3]]

    The result is [0:2, 1:3, 2:0, 3:1] with interpretation as, the 0 cubie is in the 2 cubie's position.
    '''
    def _permute(arr, p):
        '''
        Helper function to apply only one cyclic permutation.
        '''
        mod = len(p)
        temp = dict((p[x], arr[p[(x-1) % mod]]) for x, y in enumerate(p))
        out = dict((x,temp[x]) if x in temp else (x,y) for x,y in arr.items())
        return out
    if p is None:
        return d
    if type(p[0]) is list:
        for perm in p:
            d = _permute(d, perm)
    else:
        d = _permute(d, p)
    return d

move_corner = { "U": lambda self: permute(self._corner_perm, [0,1,2,3]),
                "U2": lambda self: permute(self._corner_perm, [[0,2],[1,3]]),
                "U'": lambda self: permute(self._corner_perm, [0,3,2,1]),
                "R": lambda self: permute(self._corner_perm, [2,1,5,6]),
                "R2": lambda self: permute(self._corner_perm, [[2,5],[1,6]]),
                "R'": lambda self: permute(self._corner_perm, [2,6,5,1]),
                "L": lambda self: permute(self._corner_perm, [0,3,7,4]),
                "L2": lambda self: permute(self._corner_perm, [[0,7],[4,3]]),
                "L'": lambda self: permute(self._corner_perm, [0,4,7,3]),
                "F": lambda self: permute(self._corner_perm, [3,2,6,7]),
                "F2": lambda self: permute(self._corner_perm, [[3,6],[2,7]]),
                "F'": lambda self: permute(self._corner_perm, [3,7,6,2]),
                "B": lambda self: permute(self._corner_perm, [1,0,4,5]),
                "B2": lambda self: permute(self._corner_perm, [[1,4],[0,5]]),
                "B'": lambda self: permute(self._corner_perm, [1,5,4,0]),
                "D": lambda self: permute(self._corner_perm, [7,6,5,4]),
                "D2": lambda self: permute(self._corner_perm, [0,1,2,3]),
                "D'": lambda self: permute(self._corner_perm, [7,4,5,6]),
                "M": lambda self: self._corner_perm,
                "M'": lambda self: self._corner_perm,
                "M2": lambda self: self._corner_perm,
                "E": lambda self: self._corner_perm,
                "E'": lambda self: self._corner_perm,
                "E2": lambda self: self._corner_perm,
                "S": lambda self: self._corner_perm,
                "S'": lambda self: self._corner_perm,
                "S2": lambda self: self._corner_perm}

move_edge = {   "U": lambda self: permute(self._edge_perm, [0,1,2,3]),
                "U2": lambda self: permute(self._edge_perm, [[0,2],[3,1]]),
                "U'": lambda self: permute(self._edge_perm, [0,3,2,1]),
                "R": lambda self: permute(self._edge_perm, [1,5,9,6]),
                "R2": lambda self: permute(self._edge_perm, [[1,9],[5,6]]),
                "R'": lambda self: permute(self._edge_perm, [1,6,9,5]),
                "L": lambda self: permute(self._edge_perm, [3,7,11,4]),
                "L2": lambda self: permute(self._edge_perm, [[3,11],[7,4]]),
                "L'": lambda self: permute(self._edge_perm, [3,4,11,7]),
                "F": lambda self: permute(self._edge_perm, [2,6,10,7]),
                "F2": lambda self: permute(self._edge_perm, [[2,10],[6,7]]),
                "F'": lambda self: permute(self._edge_perm, [2,7,10,6]),
                "B": lambda self: permute(self._edge_perm, [0,4,8,5]),
                "B2": lambda self: permute(self._edge_perm, [[0,8],[4,5]]),
                "B'": lambda self: permute(self._edge_perm, [0,5,8,4]),
                "D": lambda self: permute(self._edge_perm, [10,9,8,11]),
                "D2": lambda self: permute(self._edge_perm, [[10,8],[9,11]]),
                "D'": lambda self: permute(self._edge_perm, [10,11,8,9]),
                "M": lambda self: permute(self._edge_perm, [0,2,10,8]),
                "M2": lambda self: permute(self._edge_perm, [[0,10],[2,8]]),
                "M'": lambda self: permute(self._edge_perm, [0,8,10,2]),
                "E": lambda self: permute(self._edge_perm, [7,6,5,4]),
                "E2": lambda self: permute(self._edge_perm, [[7,5],[6,4]]),
                "E'": lambda self: permute(self._edge_perm, [7,4,5,6]),
                "S": lambda self: permute(self._edge_perm, [3,1,9,11]),
                "S2": lambda self: permute(self._edge_perm, [[3,9],[1,11]]),
                "S'": lambda self: permute(self._edge_perm, [3,11,9,1])}

move_center = { "M": lambda self: permute(self._edge_perm, [0,3,5,1]),
                "M2": lambda self: permute(self._edge_perm, [[0,5],[3,1]]),
                "M'": lambda self: permute(self._edge_perm, [0,1,5,3]),
                "E": lambda self: permute(self._edge_perm, [3,2,1,4]),
                "E2": lambda self: permute(self._edge_perm, [[3,1],[2,4]]),
                "E'": lambda self: permute(self._edge_perm, [3,4,1,2]),
                "S": lambda self: permute(self._edge_perm, [0,2,5,4]),
                "S2": lambda self: permute(self._edge_perm, [[0,5],[2,4]]),
                "S'": lambda self: permute(self._edge_perm, [0,4,5,2])}

orient_corners = {"R": {1:1, 5:2, 6:1, 2:2}, "R'": {1:1, 5:2, 6:1, 2:2},
                  "L": {0:2, 3:1, 7:2, 4:1}, "L'": {0:2, 3:1, 7:2, 4:1},
                  "F": {2:1, 6:2, 7:1 , 3:2}, "F'": {2:1, 6:2, 7:1, 3:2},
                  "B": {0:1, 1:2, 4:2 , 5:1}, "B'": {0:1, 1:2, 4:2 , 5:1}}
