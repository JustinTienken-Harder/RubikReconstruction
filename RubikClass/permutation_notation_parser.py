def permutation_parser(in_string, lookup = {}):
    '''
    A common cube notation for a 3-cycle is the following:
    URB -> DLF -> RBD

    This function takes such a string in, and outputs a cycle to be performed on the sticker-representation of a rubik's cube.
    '''
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
    #TODO: implement sequential commutator parser for cases like:
    # URB -> FUR -> LUB URB -> FUR -> DLR
    # remove any whitespace
    reshaped = [x.replace(" ", "") for x in split]
    reshaped = [x for x in reshaped if x != ""]
    #need first letter for orientation calls
    #first_letters = [x[0] for x in reshaped]
    modulus = len(reshaped[0])
    is_edge = modulus == 2
    if modulus != 3 or modulus != 2:
        raise "WHAT THE HECKY DECKY, UNCLEAR INPUT"
    #We now need to see if our cycle is a shift of orientation
    first = reshaped[0]
    canonical = sorted(first[0], key = sort_key)
    #this algebra allows us to deal with both corner and edge commutators
    seed_reor = sort_key(first[0]) - sort_key(canonical[0])
    if is_edge:
        if seed_reor != 0:
            seed_reor = 1
    #now we can start going through our reshaped list
    #get the current cubie representation here?

    #Helper function to get the canonical representation of a cubie, BUR becomes URB
    canon = lambda it: "".join(sorted(it, key = sort_key))
    output_cycle = [lookup[canon(first)](seed_reor%modulus)]
    if is_edge:
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
    zipped_up = zip(*output_cycle)
    return zipped_up
