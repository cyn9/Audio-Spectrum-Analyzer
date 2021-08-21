from scipy import signal


# Design Butterworth high pass filter
def designButterHPF(f_cutoff, fs, order = 5):
    """
    Returns polynomials for a digital Butterworth highpass filter.

    Parameters
    ----------
        f_cutoff : float
            Cutoff frequency of the highpass filter.
        
        fs : float
            Sampling frequency of the highpass filter.
        
        order : int
            Order of the highpass filter. Default value is 5.
    
    Returns
    -------
        b, a : ndarray
            Numerator and denominator polynomials of the Butterworth filter.
    """
    nyq = 0.5 * fs
    f_cutoff = f_cutoff / nyq
    b, a = signal.butter(order, f_cutoff, btype = 'high', analog = False)
    return b, a


# Design Butterworth bandpass filter
def designButterBPF(f_lc, f_hc, fs, order = 5):
    """
    Returns polynomials for a digital Butterworth bandpass filter.

    Parameters
    ----------
        f_lc : float
            Low cutoff frequency.

        f_hc : float
            High cutoff frequency.
        
        fs : float
            Sampling frequency of the bandpass filter.
        
        order : int
            Order of the bandpass filter. Default value is 5.
    
    Returns
    -------
        b, a : ndarray
            Numerator and denominator polynomials of the Butterworth filter.
    """
    nyq = 0.5 * fs
    low = f_lc / nyq
    high = f_hc / nyq
    b, a = signal.butter(order, [low, high], btype = 'bandpass', analog = False)
    return b, a


# Design Chebyshev Type-1 high pass filter
def designChebyshevHPF(f_cutoff, fs, rp = 0.5, order = 5):
    """
    Returns polynomials for a digital type-I Chebyshev highpass filter.

    Parameters
    ----------
        f_cutoff : float
            Cutoff frequency of the highpass filter.
        
        fs : float
            Sampling frequency of the highpass filter.
        
        rp : float
            Maximum ripple allowed below the unity gain in the passband.
            Specified in dB. Default value is 0.5 dB.
        
        order : int
            Order of the highpass filter. Default value is 5.
    
    Returns
    -------
        b, a : ndarray
            Numerator and denominator polynomials of the Chebyshev-1 filter.
    """
    nyq = 0.5 * fs
    f_cutoff = f_cutoff / nyq
    b, a = signal.cheby1(N = order, rp = rp, Wn = f_cutoff, btype = 'high', analog = False)
    return b, a


# Design Chebyshev Type-1 bandpass filter
def designChebyshevBPF(f_lc, f_hc, fs, rp = 0.5, order = 5):
    """
    Returns polynomials for a digital type-I Chebyshev bandpass filter.

    Parameters
    ----------
        f_lc : float
            Low cutoff frequency.

        f_hc : float
            High cutoff frequency.
        
        fs : float
            Sampling frequency of the bandpass filter.
        
        rp : float
            Maximum ripple allowed below the unity gain in the passband.
            Specified in dB. Default value is 0.5 dB.
        
        order : int
            Order of the bandpass filter. Default value is 5.
    
    Returns
    -------
        b, a : ndarray
            Numerator and denominator polynomials of the Chebyshev-1 filter.
    """
    nyq = 0.5 * fs
    low = f_lc / nyq
    high = f_hc / nyq
    b, a = signal.cheby1(N = order, rp = rp, Wn = [low, high], btype = 'bandpass', analog = False)
    return b, a


# Design Chebyshev Type-2 high pass filter
def designChebyshev2HPF(f_cutoff, fs, rs = 40, order = 5):
    """
    Returns polynomials for a digital type-II Chebyshev highpass filter.

    Parameters
    ----------
        f_cutoff : float
            Cutoff frequency of the highpass filter.
        
        fs : float
            Sampling frequency of the highpass filter.
        
        rs : float
            The minimum attenuation desired in the stopband. Specified in 
            dB. The default value is 40 dB.
        
        order : int
            Order of the highpass filter. Default value is 5.
    
    Returns
    -------
        b, a : ndarray
            Numerator and denominator polynomials of the Chebyshev-2 filter.
    """
    nyq = 0.5 * fs
    f_cutoff = f_cutoff / nyq
    b, a = signal.cheby2(N = order, rs = rs, Wn = f_cutoff, btype = 'high', analog = False)
    return b, a


# Design Chebyshev Type-2 bandpass filter
def designChebyshev2BPF(f_lc, f_hc, fs, rs = 40, order = 5):
    """
    Returns polynomials for a digital type-II Chebyshev bandpass filter.

    Parameters
    ----------
        f_lc : float
            Low cutoff frequency.

        f_hc : float
            High cutoff frequency.
        
        fs : float
            Sampling frequency of the bandpass filter.
        
        rs : float
            The minimum attenuation desired in the stopband. Specified in 
            dB. The default value is 40 dB.
        
        order : int
            Order of the bandpass filter. Default value is 5.
    
    Returns
    -------
        b, a : ndarray
            Numerator and denominator polynomials of the Chebyshev-2 filter.
    """
    nyq = 0.5 * fs
    low = f_lc / nyq
    high = f_hc / nyq
    b, a = signal.cheby2(N = order, rs = rs, Wn = [low, high], btype = 'bandpass', analog = False)
    return b, a


# Design Elliptic high pass filter
def designEllipticHPF(f_cutoff, fs, rp = 0.5, rs = 40, order = 5):
    """
    Returns polynomials for an Elliptic highpass filter.

    Parameters
    ----------
        f_cutoff : float
            Cutoff frequency of the highpass filter.
        
        rp : float
            The maximum ripple allowed for the highpass filter in the passband.
            The default value is 0.5 dB.
        
        rs : float
            The minimum attenuation desired in the stopband. Specified in 
            dB. The default value is 40 dB.
        
        order : int
            Order of the highpass filter. Default value is 5.
    
    Returns
    -------
        b, a : ndarray
            Numerator and denominator polynomials of the Elliptic filter.
    """
    nyq = 0.5 * fs
    f_cutoff = f_cutoff / nyq
    b, a = signal.ellip(N = order, rp = rp, rs = rs, Wn = f_cutoff, btype = 'high', analog = False)
    return b, a


# Design Elliptic bandpass filter
def designEllipticBPF(f_lc, f_hc, fs, rp = 0.5, rs = 40, order = 5):
    """
    Returns polynomials for an Elliptic bandpass filter.

    Parameters
    ----------
        f_lc : float
            Low cutoff frequency.

        f_hc : float
            High cutoff frequency.
        
        fs : float
            Sampling frequency of the bandpass filter.
        
        rp : float
            The maximum ripple allowed for the highpass filter in the passband.
            The default value is 0.5 dB.
        
        rs : float
            The minimum attenuation desired in the stopband. Specified in 
            dB. The default value is 40 dB.
        
        order : int
            Order of the bandpass filter. Default value is 5.
    
    Returns
    -------
        b, a : ndarray
            Numerator and denominator polynomials of the Elliptic filter.
    """
    nyq = 0.5 * fs
    low = f_lc / nyq
    high = f_hc / nyq
    b, a = signal.ellip(N = order, rp = rp, rs = rs, Wn = [low, high], btype = 'bandpass', analog = False)
    return b, a


# Design Bessel high pass filter
def designBesselHPF(f_cutoff, fs, order = 5):
    """
    Returns polynomials for a Bessel highpass filter.

    Parameters
    ----------
        f_cutoff : float
            Cutoff frequency of the highpass filter.
        
        fs : float
            Sampling frequency of the bandpass filter.
        
        order : int
            Order of the highpass filter. Default value is 5.
    
    Returns
    -------
        b, a : ndarray
            Numerator and denominator polynomials of the Bessel filter.
    """
    nyq = 0.5 * fs
    f_cutoff = f_cutoff / nyq
    b, a = signal.bessel(N = int(order), Wn = f_cutoff, btype = 'highpass', analog = False)
    return b, a


# Design Bessel bandpass filter
def designBesselBPF(f_lc, f_hc, fs, order = 5):
    """
    Returns polynomials for a Bessel bandpass filter.

    Parameters
    ----------
        f_lc : float
            Low cutoff frequency.

        f_hc : float
            High cutoff frequency.
        
        fs : float
            Sampling frequency of the bandpass filter.
        
        order : int
            Order of the bandpass filter. Default value is 5.
    
    Returns
    -------
        b, a : ndarray
            Numerator and denominator polynomials of the Bessel filter.
    """
    nyq = 0.5 * fs
    low = f_lc / nyq
    high = f_hc / nyq
    b, a = signal.bessel(N = int(order), Wn = [low, high], btype = 'bandpass', analog = False)
    return b, a


# Design 2nd-order IIR peak filter (only bandpass)
def designIIRPeak(f0, fs, Q = 30):
    """
    Returns polynomials for a second-order IIR peak (resonant) digital filter.

    Parameters
    ----------
        f0 : float
            Frequency to be retained in the signal.
        
        fs : float
            Sampling frequency of the IIR peak filter.

        Q : float
            Quality factor.
        
    Returns
    -------
        b, a : ndarray
            Numerator and denominator polynomials of the IIR filter.
    """
    b, a = signal.iirpeak(w0 = f0, Q = Q, fs = fs)
    return b, a
