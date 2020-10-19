def parse_wrapper(func):
    '''
    Wrapper for the permutation parser to split permuatations into components based on " & " signs in cyclic notation.

    Converts "URB -> ULF & ULB -> URF" to ['URB -> ULF', 'ULB -> URF'] and calls permutation parser on each element of this list.
    '''
    def wrapping(string_input, lookup):
        out = string_input.split(" & ")
        out = [func(x, lookup) for x in out]
        return out
    return wrapping

@parse_wrapper
def permutation_parser(in_string, lookup):
    '''
    A common cube notation for a 3-cycle is any of the equivalent formulations:
    URB -> DLF -> RBD
    URB -> DFL -> RDB
    BUR -> LDF -> BDR


    This function takes such a string in, and outputs a cycle to be performed on the cubies based on the input lookup table of a rubik's cube.
    Output looks something like a list of cycles to perform:

    [(1,2,3), (6,7,8), (9,11,12)]
    '''
    #Utilized to find the "Canonical" orientation. Representation
    sk = lambda x: (0 if (x == "U" or x == "D") \
                                    else (1 if (x == "R" or x == "L")\
                                    else 2))
    # This is all for just parsing the string into a list:
    #  URB -> DLF -> RBD into ['URB', 'DLF', 'RBD']
    if "->" not in in_string:
        if "-" in in_string:
            split = in_string.split("-")
        else:
            raise AttributeError("CANNOT PARSE NON-CYCLES")
    else:
        split = in_string.split("->")
    # remove any whitespace
    reshaped = [x.replace(" ", "") for x in split]
    reshaped = [x for x in reshaped if x != ""]    
    '''
    We have potentially many representations of the same permutation:
    
    Problem 1: Multiple representations
    URB -> FUR -> DFR -> BDR
    RUB -> RUF -> RDF -> RBD
    BUR -> URF -> FDR -> DBR
    
    Problem 2: Have to twist edges/corners:
    
    Both are in canonical representation:
    UR -> UL & UF -> UB   ==   M2 U M2 U2 M2 U M2
    (5,20) -> (3,41) & ...

    Second element needs to be flipped in permutation
(1) UR -> LU & UF -> BU   ==  (M2 U M2 U2 M2 U M2) (M' U2 M U2 M' U M U2 M' U2 M U')
    (5,20) -> (41,3) & ...
    
    Mixture of both problems: 
    RU -> LU & FU -> BU 
    (20,5) -> (41,3)

(1) RU -> UL & FU -> UB
    (20,5) -> (3,41) & ...

    '''
    #Check to see if it's a permutation on corners or edges.
    modulus = len(reshaped[0])
    if modulus != 3 and modulus != 2:
        raise AttributeError("WHAT THE HECKY DECKY, UNCLEAR INPUT TO PARSE. MUST BE CORNERS OR EDGES ONLY")
    #Helper function to get the canonical representation of a cubie, BUR becomes URB
    canon = lambda piece: "".join(sorted(piece, key = sk))
    orbit = lambda can_piece: can_piece in {"URB", "ULF", "DLB", "DRF"}
    output_cycle = []
    for string in reshaped:
        #Get canonical representation
        cs = canon(string)
        #Determine the piece's orbit
        orbital = orbit(cs)
        #determine how that piece was rotated
        rotation = cs.find(string[0])
        if orbital:
            #If it's in a different orbit, twist it in the other direction (no twists have no effects)
            rotation *= -1
        #Get the cubie and apply the rotation
        piece_index = lookup[cs](rotation)
        output_cycle.append(piece_index)
    zipped_up = zip(*output_cycle)
    return list(zipped_up)
