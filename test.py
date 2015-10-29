
import os, sys
import numpy as np
from scipy.io import wavfile
import cPickle as pickle
import scipy.io.wavfile as wav
from pylab import plt
from scipy.signal import butter, lfilter, freqz


samples_scattered = pickle.load( open( "./data/data_scattered_noLowPassed.in", "rb" ) )

samples = pickle.load( open( "./data/data_small.in", "rb" ) )

print samples['jazz'][0]
print samples_scattered['jazz'][0]


