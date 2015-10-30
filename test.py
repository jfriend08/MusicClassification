import os, sys
import numpy as np
from scipy.io import wavfile
import cPickle as pickle
import scipy.io.wavfile as wav
from pylab import plt
from scipy.signal import butter, lfilter, freqz


def generate_melbank(f1=1000, f2=8000):
  melmat, (melfreq, fftfreq) = melbank.compute_melmat(12, f1, f2, num_fft_bands=4097, sample_rate=22050)
  return melmat, (melfreq, fftfreq)
    
def plotBeforeAfterFilter(originalS, myFilter, myFilter_time, filteredS, genere, filter_idx):
  fig, (ax_orig, ax_win, ax_winT, ax_filt) = plt.subplots(4, 1, sharex=True)
  ax_orig.plot(originalS)
  ax_orig.set_title('Original pulse')
  ax_orig.margins(0, 0.1)
  ax_win.plot(myFilter)
  ax_win.set_title('str(filter_idx)'+' Filter impulse response--FrequencyDomain')
  ax_win.margins(0, 0.1)
  ax_winT.plot(myFilter_time)
  ax_winT.set_title('str(filter_idx)'+' Filter impulse response--TimeDomain')
  ax_winT.margins(0, 0.1)
  ax_filt.plot(filteredS)
  ax_filt.set_title('Filtered signal')
  ax_filt.margins(0, 0.1)
  fig.tight_layout()

def butter_lowpass(cutoff, fs, order=5):
  nyq = 0.5 * fs
  normal_cutoff = cutoff / nyq
  b, a = butter(order, normal_cutoff, btype='low', analog=False)
  return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
  b, a = butter_lowpass(cutoff, fs, order=order)
  y = lfilter(b, a, data)
  return y

order = 6
fs = 22050       # sample rate, Hz
cutoff = 8000  # desired cutoff frequency of the filter, Hz
# Get the filter coefficients so we can check its frequency response.
b, a = butter_lowpass(cutoff, fs, order)

# Plot the frequency response.
w, h = freqz(b, a, worN=8000)
plt.figure(1)
plt.subplot(411)
plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
plt.axvline(cutoff, color='k')
plt.xlim(0, 0.5*fs)
plt.title("Lowpass Filter Frequency Response")
plt.xlabel('Frequency [Hz]')
plt.grid()

T = 5.0         # seconds
n = int(T * fs) # total number of samples
t = np.linspace(0, T, n, endpoint=False)
# "Noisy" data.  We want to recover the 1.2 Hz signal from this.
data = np.sin(1.2*2*np.pi*t) + 0.5*np.sin(9000*2*np.pi*t)

# Filter the data, and plot both the original and filtered signals.
y = butter_lowpass_filter(data, cutoff, fs, order)

plt.subplot(412)
plt.plot(t, data, 'b-', label='data')
plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplots_adjust(hspace=0.35)

samples = pickle.load( open( "./data/data_small_correctFormat.in", "rb" ) )
ourSample = butter_lowpass_filter(samples['classical'][0][0], 50, 22050, 6)

plt.subplot(413)
plt.plot(samples['classical'][0][0], 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplot(414)
plt.plot(ourSample, 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()
plt.show()
