import numpy as np
from scipy import optimize

def fit_cos(xdata, ydata):
    """Positive cosine fit with FFT-based frequency estimation"""
    return _fit_cosine_general(xdata, ydata, positive=True)

def fit_cos_negative(xdata, ydata):
    """Negative cosine fit with FFT-based frequency estimation"""
    return _fit_cosine_general(xdata, ydata, positive=False)

def _fit_cosine_general(xdata, ydata, positive=True):
    """General cosine fitting function with FFT-based frequency estimation
    
    Args:
        xdata: Array of x values (heating power in mW)
        ydata: Array of y values (optical power in mW)
        positive: If True, fits A*cos(bx+c)+d; if False, fits -A*cos(bx+c)+d
    
    Returns:
        Dictionary with fit results
    """
    xdata = np.array(xdata)
    ydata = np.array(ydata)
    
    # Basic statistics for initial guesses
    guess_offset = np.mean(ydata)
    guess_amp = (np.max(ydata) - np.min(ydata)) / 2
    
    # FFT-based frequency and phase estimation
    guess_freq, fft_phase = _estimate_frequency_phase_fft(
        xdata, ydata, guess_offset, positive
    )
    
    # Build initial guess
    guess = [guess_amp, 2.*np.pi*guess_freq, fft_phase, guess_offset]
    
    # Define the cosine function based on sign
    if positive:
        def cos_func(P, A, b, c, d):
            return A * np.cos(b*P + c) + d
    else:
        def cos_func(P, A, b, c, d):
            return -A * np.cos(b*P + c) + d
    
    # Perform curve fitting
    try:
        popt, pcov = optimize.curve_fit(
            cos_func, xdata, ydata, p0=guess,
            bounds=([0, 0, -2*np.pi, -np.inf], [np.inf, np.inf, 2*np.pi, np.inf]),
            maxfev=5000
        )
    except Exception as e:
        print('fft failed 1')
        # Could add fallback strategy here
        raise
    
    A, b, c, d = popt
    
    # Normalize phase to [-π, π] then convert to [-1, 1]
    # c_normalized = np.arctan2(np.sin(c), np.cos(c)) / np.pi
    
    return A, b, c, d

def _estimate_frequency_phase_fft(xdata, ydata, offset, positive=True):
    """Estimate dominant frequency and phase using FFT
    
    Args:
        xdata: Array of x values
        ydata: Array of y values
        offset: DC offset to remove
        positive: Whether fitting positive or negative cosine
        
    Returns:
        Tuple of (frequency, phase) estimates
    """
    n = len(xdata)
    
    # Default fallback values
    default_freq = 1/20
    default_phase = 0 if positive else np.pi
    
    if n <= 10:  # Not enough points for reliable FFT
        return default_freq, default_phase
    
    try:
        # Remove DC component
        ydata_centered = ydata - offset
        
        # Create uniform spacing for FFT (interpolate if needed)
        x_uniform = np.linspace(xdata[0], xdata[-1], n)
        y_uniform = np.interp(x_uniform, xdata, ydata_centered)
        
        # Perform FFT
        fft_vals = np.fft.fft(y_uniform)
        fft_freqs = np.fft.fftfreq(n, d=(x_uniform[1] - x_uniform[0]))
        
        # Find dominant frequency (exclude DC component at index 0)
        positive_freq_indices = np.where(fft_freqs > 0)[0]
        
        if len(positive_freq_indices) == 0:
            return default_freq, default_phase
        
        # Get magnitudes for positive frequencies
        positive_fft_mags = np.abs(fft_vals[positive_freq_indices])
        
        # Find peak frequency
        peak_idx = np.argmax(positive_fft_mags)
        dominant_freq_idx = positive_freq_indices[peak_idx]
        dominant_freq = fft_freqs[dominant_freq_idx]
        
        # Get phase from FFT
        fft_phase = np.angle(fft_vals[dominant_freq_idx])
        
        # Adjust phase for negative cosine
        if not positive:
            fft_phase += np.pi
        
        # Ensure phase is in [-2π, 2π] for the bounds
        fft_phase = np.arctan2(np.sin(fft_phase), np.cos(fft_phase))

        return abs(dominant_freq), fft_phase
        
    except Exception as e:
        print('fft failed 2')
        return default_freq, default_phase
