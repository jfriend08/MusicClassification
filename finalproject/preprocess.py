import numpy as np
import random, sys
import librosa
import cPickle as pickle
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split
from  scipy.spatial.distance import euclidean
from librosa.util import normalize
from pylab import plt
from sklearn.cluster import MiniBatchKMeans

class preprocess(object):
  def getData(self, path, numDivide, **kwargs):

    clipLength = 50000

    def divideClip(clip):
      i = 0
      windowSize = int(clipLength/numDivide)
      result = []
      for count in xrange(clipLength/windowSize):
        result.append(clip[i:i+windowSize])
        i += windowSize
      return result

    selectGenre = kwargs.get('selectGenre', None)
    samples = pickle.load( open( path, "rb" ) )
    X = []
    y = []
    for genere_idx in xrange(len(samples.keys())):
      genere = samples.keys()[genere_idx]
      songs = samples[genere]
      for song_idx in xrange(len(songs)):
        song = songs[song_idx]
        # song = [clip[:clipLength] for clip in song] #some clip has different num of signal
        newSong = []
        for clip in song:
          newSong.extend(divideClip(clip))

        X.append(newSong)
        y.append(genere_idx)
    print "X size/number of songs:", len(X), "Number of clips per song:", len(X[0]), "y size:", len(y)
    return np.array(X), np.array(y)

  def featureExtraction(self, X, transpose=True):
    def MFCC(signal, sr=22050):
      return librosa.feature.mfcc(y=np.array(signal), sr=sr, n_mfcc=12)

    X = np.array([map(MFCC, song) for song in X])
    print "--> After MFCC X.shape", X.shape
    X_train_flattened = [val for sublist in X for val in sublist]
    print "--> X_train_flattened.shape", np.array(X_train_flattened).shape

    if transpose:
      X_train_flattened = np.array(map(np.transpose, X_train_flattened))
      print "--> After transpose X_train_flattened.shape", X_train_flattened.shape

    X_train_flattened_norm = normalize(X_train_flattened, norm=2)
    X_train_flattened_norm_final = np.array([mfcc for clip in X_train_flattened_norm for mfcc in clip])
    return X_train_flattened_norm_final

  def splitData(self, X, y, **kwargs):
    randState = kwargs.get('randState', 1985)
    TestTrainRatio = kwargs.get('TestTrainRatio', 0.1)
    ClassifierCenterRatio = kwargs.get('ClassifierCenterRatio', 0.6)

    rng = np.random.RandomState(randState)
    permutation = rng.permutation(len(X))
    X, y = X[permutation], y[permutation] #rand first

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TestTrainRatio, random_state=randState)
    X_train_center, X_train_classifier, y_train_center, y_train_classifier = train_test_split(X_train, y_train, test_size=ClassifierCenterRatio, random_state=randState)

    return (X_train_center, y_train_center), (X_train_classifier, y_train_classifier), (X_test, y_test)

# X, y = getData("../homework2/data/data_small8.in", 50000)
# rng = np.random.RandomState(19850920)
# permutation = rng.permutation(len(X))
# X, y = X[permutation], y[permutation]
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=2010)
# X_train_center, X_train_classifier, y_train_center, y_train_classifier = train_test_split(X_train, y_train, test_size=0.4, random_state=2010)


# X_train_center_features = featureExtraction(X_train_center) #includes MFCC and normalization
# X_train_classifier_features = featureExtraction(X_train_classifier) #includes MFCC and normalization
# print "X_train_center_features.shape", X_train_center_features.shape

# print "--------------", "START MiniBatchKMeans", "--------------"
# clf = MiniBatchKMeans(n_clusters=100,  batch_size=10000, max_iter=200).fit(X_train_center_features) #X : array-like, shape = [n_samples, n_features]
# print "clf.cluster_centers_", clf.cluster_centers_
