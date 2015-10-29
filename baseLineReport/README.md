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
![alt text](https://github.com/jfriend08/MusicClassification/blob/dev2/baseLineReport/figures/Mel_Matrix.png | width=100 "Mel_Matrix")
![alt text](https://github.com/jfriend08/MusicClassification/blob/dev2/baseLineReport/figures/mel_frequency_bank.png | width=100 "mel_frequency_bank")