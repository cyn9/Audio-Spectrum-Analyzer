from scipy import signal


# Return Hann window
def hanningWindow(M):
    return signal.windows.hann(M = M, sym = True)


# Return Hamming window
def hammingWindow(M):
    return signal.windows.hamming(M = M, sym = True)


# Return Rectangular (Boxcar) window
def rectWindow(M):
    return signal.windows.boxcar(M = M, sym = True)


# Return Kaiser window
def kaiserWindow(M, beta = 14):
    return signal.windows.kaiser(M = M, beta = beta, sym = True)


# Return Blackman window
def blackmanWindow(M):
    return signal.windows.blackman(M = M, sym = True)


# Return Flattop window
def flattopWindow(M):
    return signal.windows.flattop(M = M, sym = True)
