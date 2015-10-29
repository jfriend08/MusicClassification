from sklearn import svm, preprocessing
from sklearn.cross_validation import train_test_split
import os, sys
import numpy as np

try:
  import cPickle as pickle
except:
  import pickle

SOURCE_DIR = 'data/Data_scattered_lowPassed_energy.in'

def load_songs():
  path = os.path.join(os.getcwd(), SOURCE_DIR)
  input = open(path, 'r')
  songs = pickle.load(input)
  input.close()

  X, y = [], []
  count = 0
  for genre in songs.keys():
    for i in songs[genre].keys():
      X.append(songs[genre][i])
      y.append(count)
    count += 1

  return np.asarray(X), np.asarray(y)

def sample_preprocessing(X, y):
  rng = np.random.RandomState(5181986)
  minMaxScaler = preprocessing.MinMaxScaler((-1, 1))
  X = minMaxScaler.fit_transform(X, y)

  permutation = rng.permutation(len(X))
  return train_test_split(X[permutation], y[permutation], train_size=0.5, random_state=0)

if __name__ == '__main__':
  X, y = load_songs()
  train_x, test_x, train_y, test_y = sample_preprocessing(X, y)

  clf = svm.SVC(degree=2)
  clf.fit(train_x, train_y)

  print clf.score(train_x, train_y)
  print clf.score(test_x, test_y)
