import os, sys
import numpy as np
from scipy.io import wavfile
import cPickle as pickle
import scipy.io.wavfile as wav
from pylab import plt

''' pyfilterbank '''
sys.path.append('./pyfilterbank/pyfilterbank')
import melbank

def generate_melbank():
  '''
  @return: melmat, (num_mel_bands, num_fft_bands)

  melmat: Transformation matrix for the mel spectrum. Use this with fft spectra of num_fft_bands_bands length
          and multiply the spectrum with the melmat this will tranform your fft-spectrum to a mel-spectrum.
  num_mel_bands: Center frequencies of the mel bands
  num_fft_bands: center frequencies of fft spectrum
  '''
  f1, f2 = 1000, 8000 #low and high frequency range
  #use the same sampling rate and numbers of frequency bank
  melmat, (melfreq, fftfreq) = melbank.compute_melmat(12, f1, f2, num_fft_bands=4097, sample_rate=22050)
  fig, ax = plt.subplots(figsize=(8, 3))
  ax.plot(fftfreq, melmat.T)
  ax.grid(True)
  ax.set_ylabel('Weight')
  ax.set_xlabel('Frequency / Hz')
  ax.set_xlim((f1, f2))
  ax2 = ax.twiny()
  ax2.xaxis.set_ticks_position('top')
  ax2.set_xlim((f1, f2))
  ax2.xaxis.set_ticks(melbank.mel_to_hertz(melfreq))
  ax2.xaxis.set_ticklabels(['{:.0f}'.format(mf) for mf in melfreq])
  ax2.set_xlabel('Frequency / mel')
  plt.tight_layout()

  fig, ax = plt.subplots()
  ax.matshow(melmat)
  plt.axis('equal')
  plt.axis('tight')
  plt.title('Mel Matrix')
  plt.tight_layout()
  # plt.show()

  return melmat, (melfreq, fftfreq)

def plotBeforeAfterFilter(originalS, myFilter, filteredS):
  fig, (ax_orig, ax_win, ax_filt) = plt.subplots(3, 1, sharex=True)
  ax_orig.plot(originalS)
  ax_orig.set_title('Original pulse')
  ax_orig.margins(0, 0.1)
  ax_win.plot(myFilter)
  ax_win.set_title('Filter impulse response')
  ax_win.margins(0, 0.1)
  ax_filt.plot(filteredS)
  ax_filt.set_title('Filtered signal')
  ax_filt.margins(0, 0.1)
  fig.tight_layout()
  fig.show()

def convolve(arrays, melBank, genera):
  x = []
  m = np.asmatrix(np.array(x))
  for eachClip in arrays:
    result = np.convolve(eachClip, melBank)
    x.append(result)
    m = np.asmatrix(np.array(x))
    plotBeforeAfterFilter(eachClip, melBank, result)
  fig, ax = plt.subplots()
  ax.matshow(m)
  plt.axis('equal')
  plt.axis('tight')
  plt.title(genera)
  plt.tight_layout()
  plt.show()


if __name__ == '__main__':
  melmat, (melfreq, fftfreq) = generate_melbank()

  samples = pickle.load( open( "./data/data.in", "rb" ) )
  for key in samples.keys():
    print "now process", key, "song1"
    convolve(samples[key][0], melmat[0], key)