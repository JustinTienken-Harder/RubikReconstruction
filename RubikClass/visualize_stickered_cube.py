import numpy as np


def pixel_value_sticker(sticker_array = None, bandw = False):
    if sticker_array is None:
        stickers = list("w"*9+"b"*9+"r"*9+"g"*9+"o"*9+"y"*9)
    else:
        stickers = sticker_array
    #Get the whole thingy majig
    if bandw:
        color_remap= {"w":[1],"b":[2/7],"r":[3/7],"g":[4/7],"o":[5/7],"y":[6/7],"e":[1/7],"":[0]}
        channels = 1
    else:
        color_remap = {"w":[255,255,255],"b":[0,0,255],"r":[255,0,0],"g":[0,255,0],
                       "o":[255,165,0],"y":[255,255,0],"e":[128,128,128],"":[0,0,0]}
        channels = 3
    #stickies = [color_remap[x] for x in stickers]
    out = []
    stickies = [color_remap[x] for x in stickers]
    for k in range(1,3):
        for j in range(3):
            if k == 2:
                hmm = stickies[(27+3*j):(30+j*3)].copy()
                hmm.extend(stickies[(36+3*j):(39+j*3)])
                hmm.extend(stickies[(45+3*j):(48+j*3)])
                out.append(hmm)
            else:
                hmm = stickies[(0+3*j):(3+j*3)].copy()
                hmm.extend(stickies[(9+3*j):(12+j*3)])
                hmm.extend(stickies[(18+3*j):(21+j*3)])
                out.append(hmm)
    return np.array(out)
