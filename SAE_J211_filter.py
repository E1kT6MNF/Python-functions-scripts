def SAE_J211_filter(y, COFreq,DeltaTime):
    import numpy as np
    # This function applies 2nd order Butterworth low pass filter per SAE J211.
    # Arguments:
    #   y = array of signal data
    #   COFreq = -3db cutoff frenquency of filter
    #   DeltaTime = signal time increment in seconds
    # Output: same struct with filtered "y" data
    # Author: John Newkirk
    #
    # This Function is a second order Butterworth digital filter using forward and
    #  backward passes to remove phase shift.  The algorithm was copied from the SAE
    #  J 2238 APPENDIX D.
    # This function is a MATLAB translarion of the EDAPT PASCAL code.
    # 
    n = np.size(y)
    # Check to see if the forward or reverse coefficients are less than
    # the inverse of 5 times DeltaTime.  5 Points define a full sine wave.
    # The lowest frequency measurable = 1/(5*DeltaTime).  A roll off any
    # smaller than this would not effect the curve.
    if COFreq <= (1/(5*DeltaTime)):
        ## Computing Filter Coefficients
        Fm6db = 1.25 * COFreq
        wd = 2 * Fm6db * np.pi
        wa = np.sin(wd * DeltaTime / 2.0) / np.cos(wd * DeltaTime / 2.0)
        b0 = wa**2/(1.0 + np.sqrt(2.0) * wa + wa**2)
        b1 = 2.0 * b0
        b2 = b0
        a1 = -2.0 * (wa**2 - 1.0)/(1.0 + np.sqrt(2.0) * wa + wa**2)
        a2 = (-1.0 + np.sqrt(2.0) * wa - wa**2)/(1.0 + np.sqrt(2.0) * wa + wa**2)
    
        # Filter Forward
        y1 = np.mean(y[0:10]) #average the first ten
        x1 = y[0] #Save the first array value
        x0 = y[1] #Save the second array value
        y[0:2] = y1           #reassign the first and second array values to the avg
    
        for Index in range(2,n):  #start from the third array value
            x2 = x1
            x1 = x0
            x0 = y[Index]
            y[Index] = b0 * x0 + b1 * x1 + b2 * x2 + a1 * y[Index - 1] + a2 * y[Index - 2]
    
    
        # Filter Backwards
        y1 = np.mean(y[n-10:])
        x1 = y[n-1]
        x0 = y[n-2]
        y[n-1] = y1
        y[n-2] = y1
       
        for Index in range(n-3,-1,-1):
            x2 = x1
            x1 = x0
            x0 = y[Index]
            y[Index]= b0*x0 + b1*x1 + b2*x2 + a1*y[Index+1] + a2*y[Index + 2]
    
    else:
        print('Error: Filter frequency is incompatible with sample rate')
    
    return y      

    
    
    