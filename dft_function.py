import math
def dft(x):
    #Formula da DFT usada como base
    N = len(x)
    X = [0] * N
    
    for k in range(N):
        re = 0
        im = 0
        for n in range(N):
            phi = (2*math.pi*k*n)/N
            re += x[n]*math.cos(phi)
            im -= x[n]*math.sin(phi)
        re = re/N
        im = im/N
        
        freq = k
        amp = math.sqrt(re*re+im*im)
        phase = math.atan2(im, re)
        X[k] = [re, im, freq, amp, phase]
    return X