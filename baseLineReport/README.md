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
* To check the effect of convolution, this is the experiment to visualize the signal before and after convolution of one certain filter bank. So here attached the last clip of first song in disco genere that being convoluted by last filter bank which the frequency roughly ranged from 4000 to 6000 Hz. By comparing the signal before and after convolution, we can see the signal magnitude droped from about 10,000 to 1,000, implying the convolution process plays a role in removing most of signal outside filter bank, and, therefore, the magnitude after convolution dropped.
* On the other hand, although not precisely measured, we can also noticed the signal before convolution may contain lower frequency of signal because there are wider gaps between signal peak to peak, but the gap narrowed after convolution, which may imply lower frequency of signal being removed
* The second figure is composit signal heapmat of every clips from first disco music being convoluted
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

###Effect of lowpass filter
* To visualize the effect of lowpass filter, here we did experiment on two approaches. One is creating a signal wih noise append, and the other one is use the real clip from our sample, see what is the effect if the signal being low passed
* From the first figure attached, we designed a order of 6 lowpassed filter with 8000Hz cutoff and 22050Hz sampling rate. Then we created a signal with 1.2Hz combined with 9000Hz noise appened. Since frequency of noise is very high, so we can see there are lots of high-frequent ripples along the curve of the 1.2Hz signal. Then, after lowpass filtered, signal became cleaners but can still noticed certain ripples. I think this is due to the lowpass will never being able to cutoff at 8000Hz sharp, but a curve gradually decrease to 0, therefore there are signal between 8000 to 9000 that still existed in the signal.
* Since our mel-frequency banks ranged from 0 to 6000Hz, we decide to design a order of 6 lowpass filter with 6500Hz cutoff for our project
* Then, we tested one the signal from one of the clip and performed lowpass. As we can see from the second attached figure, there are lots of high frequent signals being removed, and leave cleaner signal with lower magnitude

```python
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

T = 5.0         # seconds
n = int(T * fs) # total number of samples
t = np.linspace(0, T, n, endpoint=False)
# "Noisy" data.  We want to recover the 1.2 Hz signal from this.
data = np.sin(1.2*2*np.pi*t) + 0.5*np.sin(9000*2*np.pi*t)

# Filter the data, and plot both the original and filtered signals.
y = butter_lowpass_filter(data, cutoff, fs, order)

plt.subplot(2, 1, 2)
plt.plot(t, data, 'b-', label='data')
plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplots_adjust(hspace=0.35)
plt.show()

```

![alt text](https://github.com/jfriend08/MusicClassification/blob/dev2/baseLineReport/figures/lowPassButterFilter.png "lowPassButterFilter")
![alt text](https://github.com/jfriend08/MusicClassification/blob/dev2/baseLineReport/figures/FilterFigure_classical.png "FilterFigure_classical")

###Scattering procedures
* To demonstrate the procedures of signal scattering in high-level point of view, here are the codes from signalScattering.py
```python
if __name__ == '__main__':
  '''Get my mel-frequency bank'''
  melmat, (melfreq, fftfreq) = generate_melbank(0, 6000)

  '''Transfrom mel-frequency to time domain'''
  melmat_time = freq2timeDomain(melmat)

  '''Read in data'''
  samples = pickle.load( open( "./data/data.in", "rb" ) )

  '''Example of performing lowpass on given signal'''
  y = butter_lowpass_filter(samples_small['classical'][0][0], 50, 22050, 6)

  '''samples_small_scattered will be the scattered result (plus lowpass filtered) from samples_small'''
  samples_small_scattered = scatteringHandler(melmat_time, samples_small)

```


