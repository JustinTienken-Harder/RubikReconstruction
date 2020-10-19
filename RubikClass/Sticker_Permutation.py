def permute_list_immutable(A, P):
    '''
    Given a string (or list) and cyclic representation of a permutation P, permute the elements in A by the indeces described in permutation P
    
    This is actually a bit slower than the mutable version.
    '''
    #Use recursion on list of cycles to perform
    if type(P[0]) is tuple or type(P[0]) is list:
        for permutation in P:
            A = permute_list_immutable(A, permutation)
        return A
    lu = dict((y,x) for x,y in enumerate(P))
    permuted = "".join(A[P[lu[i]-1]] if i in P else x for i, x in enumerate(A))
    return permuted

def permute_list_mutable(A, P):
    '''
    Given a list, A, and cyclic representation of a permutation, P, permute the elements in A by the indices described in permutation P.

    If P was (1,3,5,7), it would be the following reassignment:
    A[1], A[3], A[5], A[7] = A[7], A[1], A[3], A[5],

    Faster implementation that utilizes the mutability of lists to get aprox 2x-3x faster results than immutable
    '''
    #Use recursion on list of cycles to perform
    if type(P[0]) is tuple or type(P[0]) is list:
        for permutation in P:
            permute_list_mutable(A, permutation)
        return
    swaps = [(P[i-1],P[i]) for i, _ in enumerate(P)]
    for start,target in reversed(swaps[1:]): 
        A[target], A[start] = A[start], A[target]



if __name__ == "__main__":
    import timeit 
    a = list('w'*9+'b'*9+"r"*9+"g"*9+'o'*9+'y'*9)
    u_p = [(5, 1, 3, 7), (21, 16, 41, 28), (2, 0, 6, 8), (18, 15, 44, 29), (17, 38, 27, 24)]
    m_p = [(7, 16, 52, 34), (28, 1, 10, 46), (4, 13, 49, 31)]
    permute_list_mutable(a, u_p)
    print(a)
    permute_list_mutable(a, m_p)
    print(a)
    setup2 = '''A = "abcdefghi" \nP = (1,3,5,7)'''
    code2 = '''lu = dict((y,x) for x,y in enumerate(P))\npermuted = "".join(A[P[lu[i]-1]] if i in P else x for i, x in enumerate(A))'''
    print(timeit.timeit(code2, setup2))

    setup="""A = ["a", 'b', 'c','d','e','f','g','h','i']\nP = (1,3,5,7)"""
    code = '''
swaps = [(P[i-1],P[i]) for i, _ in enumerate(P)]
for start,target in reversed(swaps[1:]): 
    A[target], A[start] = A[start], A[target]
'''
    print(timeit.timeit(code, setup))