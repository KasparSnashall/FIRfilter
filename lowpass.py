from pylab import *
import scipy.signal as signal


numtaps = 201 # number of coeffs
#cut off is the normalised cut off in terms of nqy
# window is the function


# options = boxcar, triang, blackman, hamming, hann, bartlett, flattop, parzen, bohman, blackmanharris, nuttall, barthann, kaiser (needs beta), gaussian (needs standard deviation), general_gaussian (needs power, width), slepian (needs width), chebwin (needs attenuation), exponential (needs decay scale), tukey (needs taper fraction)

fir_coeff = signal.firwin(numtaps, cutoff = 0.2, window = ("gaussian",6), nyq = 500E3)


def mfreqz(b,a=1):
    w,h = signal.freqz(b,a)
    h_dB = 20 * log10 (abs(h))
    subplot(111)
    plot(w/max(w),h_dB)
    ylim(-150, 5)
    ylabel('Magnitude (db)')
    xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
    title(r'Frequency response')






mfreqz(fir_coeff)
show()
