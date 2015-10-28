import os, sys
import numpy as np
from scipy.io import wavfile
import cPickle as pickle
import scipy.io.wavfile as wav
from pylab import plt
from scipy.signal import butter, lfilter, freqz

''' pyfilterbank '''
sys.path.append('./pyfilterbank/pyfilterbank')
import melbank

def generate_melbank(f1=1000, f2=8000):
  '''
  @INPUT: low and high frequency range
  @RETURN: melmat, (num_mel_bands, num_fft_bands)
  melmat: Transformation matrix for the mel spectrum. Use this with fft spectra of num_fft_bands_bands length
          and multiply the spectrum with the melmat this will tranform your fft-spectrum to a mel-spectrum.
  num_mel_bands: Center frequencies of the mel bands
  num_fft_bands: center frequencies of fft spectrum
  '''
  # f1, f2 = 1000, 8000 #low and high frequency range
  #use the same sampling rate and numbers of frequency bank
  melmat, (melfreq, fftfreq) = melbank.compute_melmat(12, f1, f2, num_fft_bands=4097, sample_rate=22050)
  # fig, ax = plt.subplots(figsize=(8, 3))
  # ax.plot(fftfreq, melmat.T)
  # ax.grid(True)
  # ax.set_ylabel('Weight')
  # ax.set_xlabel('Frequency / Hz')
  # ax.set_xlim((f1, f2))
  # ax2 = ax.twiny()
  # ax2.xaxis.set_ticks_position('top')
  # ax2.set_xlim((f1, f2))
  # ax2.xaxis.set_ticks(melbank.mel_to_hertz(melfreq))
  # ax2.xaxis.set_ticklabels(['{:.0f}'.format(mf) for mf in melfreq])
  # ax2.set_xlabel('Frequency / mel')
  # plt.tight_layout()

  # fig, ax = plt.subplots()
  # ax.matshow(melmat)
  # plt.axis('equal')
  # plt.axis('tight')
  # plt.title('Mel Matrix')
  # plt.tight_layout()

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
  filename = "./figures/filterBeforeAfter/FilterFigure_"+"Filter"+str(filter_idx)+genere+".png"
  fig.savefig(filename)
  # fig.show()

def convolve(arrays, melBank, genere, filter_idx):
  x = []
  melBank_time = np.fft.ifft(melBank) #need to transform melBank to time domain
  for eachClip in arrays:
    result = np.convolve(eachClip, melBank_time)
    x.append(result)
    # plotBeforeAfterFilter(eachClip, melBank, melBank_time, result, genere, filter_idx)

  # m = np.asmatrix(np.array(x))
  # fig, ax = plt.subplots()
  # ax.matshow(m.real) #each element has imaginary part. So just plot real part
  # plt.axis('equal')
  # plt.axis('tight')
  # plt.title(genere)
  # plt.tight_layout()
  # filename = "./figures/convolution/Convolution_"+"Filter"+str(filter_idx)+genere+".png"
  # plt.savefig(filename)
  # plt.show()
def freq2timeDomain(melmat):
  result = []
  for melBank in melmat:
    melBank_time = np.fft.ifft(melBank)
    result.append(melBank_time)
  return np.array(result)

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff=6500, fs=22050, order=6):
  '''
  @INPUT:
  data- data wanna be filtered. This could be just one list
  cutoff- cutoff frequency wanna filtered. in Hz
  fs- sampling rate. default is 22050. Same as the paper used
  order- the order of butter lowpass filter. the higher the order, the sharper at the edge
  @RETURN:
  just the filtered signal in the same structure as data (list)
  '''
  b, a = butter_lowpass(cutoff, fs, order=order)
  y = lfilter(b, a, data)
  return y

def sampleSplit(samples, splitNum):
  result = {}
  for genere in samples.keys():
    mylists = []
    mylists.append(samples[genere][0])
    mylists.append(samples[genere][1])
    result[genere] = mylists
  return result

def scattering(song, melmat_time):
  print "Start: scattering for current song"
  print "Before: length for this song", len(song)
  resultForThisSong = []
  for clip_0order in song:
    resultForThisSong.append(clip_0order) #append zero order
    for filter_idx1 in range(len(melmat_time)):
      melBank1 = melmat_time[filter_idx1]
      clip_1order = np.convolve(clip_0order, melBank1)
      resultForThisSong.append(clip_1order) #append first order
      for filter_idx2 in range(filter_idx1+1, len(melmat_time)):
        melBank2 = melmat_time[filter_idx2]
        clip_2order = np.convolve(clip_1order, melBank2)
        resultForThisSong.append(clip_2order) #append second order
  song = map(butter_lowpass_filter, resultForThisSong)
  # butter_lowpass_filter(resultForThisSong, 6500, 22050, 6)
  # song = resultForThisSong
  print "After: length for this song", len(song)
  return song

def scatteringHandler(melmat_time, samples_small):
  '''
  @INPUT:
  melmat_time: mel-frequency bank in time domain. list of list
  samples_small: map of list of list of list. key is the genere, value is list songs, each song has list of clips
  @RETURN:
  each song doesn't contain list of clips anymore, but the scattered results with convoluted with lowpass.
  structure still map of list of list of list

  Before: length for this song 10
  After: length for this song 790
  '''
  for genere in samples_small.keys():
    samples = samples_small[genere];
    for song in samples:
      song = scattering(song, melmat_time)
  return samples_small


if __name__ == '__main__':
  '''Get my mel-frequency bank'''
  melmat, (melfreq, fftfreq) = generate_melbank(0, 6000)

  '''Transfrom mel-frequency to time domain'''
  melmat_time = freq2timeDomain(melmat)

  '''Read in data'''
  # samples = pickle.load( open( "./data/data.in", "rb" ) )
  samples_small = pickle.load( open( "./data/data_small.in", "rb" ) )

  '''Example of performing lowpass on given signal'''
  y = butter_lowpass_filter(samples_small['classical'][0][0], 50, 22050, 6)

  '''samples_small_scattered will be the scattered result from samples_small'''
  samples_small_scattered = scatteringHandler(melmat_time, samples_small)
  o = open('./data/data_scattered.in', 'w')
  pickle.dump(samples_small_scattered, o)
  o.close()




  # for key in samples_small.keys():
  #   print "now process", key, "song1"
  #   for eachFilter_idx in xrange(len(melmat)):
  #     eachFilter = melmat[eachFilter_idx]
  #     convolve(samples_small[key][0], eachFilter, key, eachFilter_idx)

  # plotBeforeAfterFilter(samples_small['classical'][0][0], melmat[0], np.fft.ifft(melmat[0]), y, "classical")

  # plt.subplot(1, 1, 1)
  # plt.plot(samples_small['classical'][0][0])
  # # plt.plot(samples_small['classical'][0][0], 'b-', label='data')
  # plt.subplot(1, 1, 2)
  # plt.plot(y, 'g-', linewidth=2, label='filtered data')
  # plt.xlabel('Time [sec]')
  # plt.grid()
  # plt.legend()
  # plt.subplots_adjust(hspace=0.35)
  # plt.show()