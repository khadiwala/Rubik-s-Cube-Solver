import numpy

def calc_cof():
    #original 4 points
    facesize = 30
    nw = (0,0)
    ne = (facesize,0)
    sw = (0,facesize)
    se = (facesize,facesize)

    #maps to
    mnw = (facesize/3,facesize/3)
    mne = (facesize/3,(2*facesize)/3)
    msw = (0,facesize)
    mse = (facesize,facesize)

    G = numpy.array([ [nw[0],nw[1],1,0,0,0,-nw[0]*mnw[0],-nw[1]*mnw[0]],
          [ne[0],ne[1],1,0,0,0,-ne[0]*mne[0],-nw[1]*mne[0]],
          [sw[0],sw[1],1,0,0,0,-sw[0]*msw[0],-sw[1]*msw[0]],
          [se[0],se[1],1,0,0,0,-se[0]*mse[0],-se[1]*mse[0]],
          [0, 0, 0, nw[0],nw[1],1,-nw[0]*mnw[0],-nw[0]*mnw[1]],
          [0, 0, 0, ne[0],ne[1],1,-ne[0]*mne[0],-ne[0]*mne[1]],
          [0, 0, 0, sw[0],sw[1],1,-sw[0]*msw[0],-sw[0]*msw[1]],
          [0, 0, 0, se[0],se[1],1,-se[0]*mse[0],-se[0]*mse[1]] ])

    d = numpy.transpose([mnw[0],mne[0],msw[0],mse[0],mnw[1],mne[1],msw[1],mse[1]])
    m = numpy.linalg.solve(G,d)

    p = tuple(m)

    return m
