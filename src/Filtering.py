from scipy import signal


# Design Butterworth high pass filter
def designButterHPF(f_cutoff, fs, order = 5):
    nyq = 0.5 * fs
    f_cutoff = f_cutoff / nyq
    b, a = signal.butter(order, f_cutoff, btype = 'high', analog = False)
    return b, a


# Design Butterworth bandpass filter
def designButterBPF(f_lc, f_hc, fs, order = 5):
    nyq = 0.5 * fs
    low = f_lc / nyq
    high = f_hc / nyq
    b, a = signal.butter(order, [low, high], btype = 'bandpass', analog = False)
    return b, a


# Design Chebyshev Type-1 high pass filter
def designChebyshevHPF(f_cutoff, fs, rp = 0.5, order = 5):
    nyq = 0.5 * fs
    f_cutoff = f_cutoff / nyq
    b, a = signal.cheby1(N = order, rp = rp, Wn = f_cutoff, btype = 'high', analog = False)
    return b, a


# Design Chebyshev Type-1 bandpass filter
def designChebyshevBPF(f_lc, f_hc, fs, rp = 0.5, order = 5):
    nyq = 0.5 * fs
    low = f_lc / nyq
    high = f_hc / nyq
    b, a = signal.cheby1(N = order, rp = rp, Wn = [low, high], btype = 'bandpass', analog = False)
    return b, a


# Design Chebyshev Type-2 high pass filter
def designChebyshev2HPF(f_cutoff, fs, rs = 40, order = 5):
    nyq = 0.5 * fs
    f_cutoff = f_cutoff / nyq
    b, a = signal.cheby2(N = order, rs = rs, Wn = f_cutoff, btype = 'high', analog = False)
    return b, a


# Design Chebyshev Type-2 bandpass filter
def designChebyshev2BPF(f_lc, f_hc, fs, rs = 40, order = 5):
    nyq = 0.5 * fs
    low = f_lc / nyq
    high = f_hc / nyq
    b, a = signal.cheby2(N = order, rs = rs, Wn = [low, high], btype = 'bandpass', analog = False)
    return b, a


# Design Elliptic high pass filter
def designEllipticHPF(f_cutoff, fs, rp = 0.5, rs = 40, order = 5):
    nyq = 0.5 * fs
    f_cutoff = f_cutoff / nyq
    b, a = signal.ellip(N = order, rp = rp, rs = rs, Wn = f_cutoff, btype = 'high', analog = False)
    return b, a


# Design Elliptic bandpass filter
def designEllipticBPF(f_lc, f_hc, fs, rp = 0.5, rs = 40, order = 5):
    nyq = 0.5 * fs
    low = f_lc / nyq
    high = f_hc / nyq
    b, a = signal.ellip(N = order, rp = rp, rs = rs, Wn = [low, high], btype = 'bandpass', analog = False)
    return b, a


# Design Bessel high pass filter
def designBesselHPF(f_cutoff, fs, order = 5):
    nyq = 0.5 * fs
    f_cutoff = f_cutoff / nyq
    b, a = signal.bessel(N = int(order), Wn = f_cutoff, btype = 'highpass', analog = False)
    return b, a


# Design Bessel bandpass filter
def designBesselBPF(f_lc, f_hc, fs, order = 5):
    nyq = 0.5 * fs
    low = f_lc / nyq
    high = f_hc / nyq
    b, a = signal.bessel(N = int(order), Wn = [low, high], btype = 'bandpass', analog = False)
    return b, a


# Design 2nd-order IIR peak filter (only bandpass)
def designIIRPeak(f0, fs, Q = 30):
    b, a = signal.iirpeak(w0 = f0, Q = Q, fs = fs)
    return b, a

