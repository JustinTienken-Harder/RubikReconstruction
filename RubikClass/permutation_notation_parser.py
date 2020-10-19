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
    #Utilized to find the "Canonical" orientation. Tells a cubie how to be rotated.
    sort_key = lambda x: (0 if (x == "U" or x == "D") \
                                    else (1 if (x == "R" or x == "L")\
                                    else 2))
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
    #need first letter for orientation calls
    #first_letters = [x[0] for x in reshaped]
    modulus = len(reshaped[0])
    is_edge = modulus == 2
    if modulus != 3 and modulus != 2:
        raise AttributeError("WHAT THE HECKY DECKY, UNCLEAR INPUT TO PARSE. MUST BE CORNERS OR EDGES ONLY")
    #We now need to see if our cycle is a shift of orientation
    first = reshaped[0]
    canonical = sorted(first[0], key = sort_key)
    #this algebra allows us to deal with both corner and edge commutators
    seed_reor = sort_key(first[0]) - sort_key(canonical[0])
    if is_edge:
        if seed_reor != 0:
            seed_reor = 1
    #now we can start going through our reshaped list

    #Helper function to get the canonical representation of a cubie, BUR becomes URB
    canon = lambda it: "".join(sorted(it, key = sort_key))
    #lookup[canon(first)] gets the canonical representation of a cubie while (seed_reor%modulus) "rotates" it according to the input 
    output_cycle = [lookup[canon(first)](seed_reor%modulus)]
    if is_edge: #have to deal with corner/edge commutators seperately
        for piece in reshaped[1:]:
            piece_canon = canon(piece)
            if piece == piece_canon:
                rel_reor = 0
            else:
                rel_reor = 1
            total_reor = (seed_reor + rel_reor)%modulus
            out_cubie = lookup[piece_canon](total_reor)
            output_cycle.append(out_cubie)
    else:
        for piece in reshaped[1:]:
            #Have to get relative reorientation
            rel_reor = sort_key(piece[0])
            total_reor = (seed_reor + rel_reor)%modulus
            out_cubie = lookup[piece_canon](total_reor)
            output_cycle.append(out_cubie)
    #we now have a list of [[1,2], [3,4], [5,6]], but we actually want to send stickers 1->3->5 and 2->4->6
    #so we zip up the list. 
    zipped_up = zip(*output_cycle)
    return list(zipped_up)
