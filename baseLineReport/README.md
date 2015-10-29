# Experiments
###Mel Filter Bank
* This is the experiments to visualize the generated filter banks. As we tryig to reproduce our reference papers' result, we set up the lower and upper bound of filter frequency to 0 to 6000 Hz, being covered by 12 filters with 22050Hz sampling rate (same as sampling rate of each clip)
* As you can see, it generated filter banks with triangular shaped bands ranged on the mel frequency scale
```python
def generate_melbank(lowBound=1000, highBound=8000):
  melmat, (melfreq, fftfreq) = melbank.compute_melmat(12, lowBound, highBound, num_fft_bands=4097, sample_rate=22050)
  fig, ax = plt.subplots(figsize=(8, 3))
  ax.plot(fftfreq, melmat.T)
  ax.grid(True)
  ax.set_ylabel('Weight')
  ax.set_xlabel('Frequency / Hz')
  ax.set_xlim((lowBound, highBound))
  ax2 = ax.twiny()
  ax2.xaxis.set_ticks_position('top')
  ax2.set_xlim((lowBound, highBound))
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
  plt.show()
  return melmat, (melfreq, fftfreq)

generate_melbank(0, 6000)
```
![alt text](https://github.com/jfriend08/MusicClassification/blob/dev2/baseLineReport/figures/Mel_Matrix.png "Mel_Matrix")
![alt text](https://github.com/jfriend08/MusicClassification/blob/dev2/baseLineReport/figures/mel_frequency_bank.png "mel_frequency_bank")


###Effect of convolution

```python
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

def convolve(arrays, melBank, genere, filter_idx):
  x = []
  melBank_time = np.fft.ifft(melBank) #need to transform melBank to time domain
  for eachClip in arrays:
    result = np.convolve(eachClip, melBank_time)
    x.append(result)
    plotBeforeAfterFilter(eachClip, melBank, melBank_time, result, genere, filter_idx)

  m = np.asmatrix(np.array(x))
  fig, ax = plt.subplots()
  ax.matshow(m.real) #each element has imaginary part. So just plot real part
  plt.axis('equal')
  plt.axis('tight')
  plt.title(genere)
  plt.tight_layout()
  plt.show()

for key in samples.keys():
  print "now process", key, "song1"
  for eachFilter_idx in xrange(len(melmat)):
    eachFilter = melmat[eachFilter_idx]
    convolve(samples[key][0], eachFilter, key, eachFilter_idx)
```
![alt text](https://github.com/jfriend08/MusicClassification/blob/dev2/baseLineReport/figures/FilterFigure_Filter11disco.png "FilterFigure_Filter11disco")
![alt text](https://github.com/jfriend08/MusicClassification/blob/dev2/baseLineReport/figures/Convolution_Filter11disco.png "Convolution_Filter11disco")