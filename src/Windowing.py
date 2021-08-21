from scipy import signal


def hanningWindow(M):
    """
    Returns a Hanning window.

    Parameters
    ----------
        M : int
            Number of points in the output window.
    
    Returns
    -------
        w : ndarray
            Hann window.
    """
    assert M > 0, 'ERROR: Non-positive M value..'
    return signal.windows.hann(M = M, sym = True)


def hammingWindow(M):
    """
    Returns a Hamming window.

    Parameters
    ----------
        M : int
            Number of points in the output window.
    
    Returns
    -------
        w : ndarray
            Hamming window.
    """
    assert M > 0, 'ERROR: Non-positive M value..'
    return signal.windows.hamming(M = M, sym = True)


def rectWindow(M):
    """
    Returns a rectangular (Dirichlet or boxcar) window. 
    Equivalent to no window at all.

    Parameters
    ----------
        M : int
            Number of points in the output window.
    
    Returns
    -------
        w : ndarray
            Rectangular window.
    """
    assert M > 0, 'ERROR: Non-positive M value..'
    return signal.windows.boxcar(M = M, sym = True)


def kaiserWindow(M, beta = 14):
    """
    Returns a Kaiser window.

    Parameters
    ----------
        M : int
            Number of points in the output window.
        
        beta : float
            Shape parameter that determines trade-off between main lobe
            width and side lobe level. Higher the beta, narrow the window.
            The default value is 14.
    
    Returns
    -------
        w : ndarray
            Kaiser window.
    """
    assert M > 0, 'ERROR: Non-positive M value..'
    assert beta > 0, 'ERROR: Non-positive beta value.'

    return signal.windows.kaiser(M = M, beta = beta, sym = True)


def blackmanWindow(M):
    """
    Returns a Blackman window.

    Parameters
    ----------
        M : int
            Number of points in the output window.
        
    Returns
    -------
        w : ndarray
            Blackman window.
    """
    assert M > 0, 'ERROR: Non-positive M value..'
    return signal.windows.blackman(M = M, sym = True)


def flattopWindow(M):
    """
    Returns a Flattop window.

    Parameters
    ----------
        M : int
            Number of points in the output window.
        
    Returns
    -------
        w : ndarray
            Flattop window.
    """
    assert M > 0, 'ERROR: Non-positive M value..'
    return signal.windows.flattop(M = M, sym = True)
