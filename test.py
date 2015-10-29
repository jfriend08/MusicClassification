
import os, sys
import numpy as np
from scipy.io import wavfile
import cPickle as pickle
import scipy.io.wavfile as wav
from pylab import plt
from scipy.signal import butter, lfilter, freqz


samples_scattered = pickle.load( open( "./data/Data_scattered_lowPassed_energy.in", "rb" ) )

samples = pickle.load( open( "./data/data_small_correctFormat.in", "rb" ) )

print samples['jazz'][0]
print samples_scattered['jazz'][0]


