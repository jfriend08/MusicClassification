import preprocess_newVLAD as preprocess
import cProfile
import argparse
from sklearn.decomposition import PCA

parser = argparse.ArgumentParser()
parser.add_argument("numDivide", help="number of split of each clip. e.g. 3 then each clip will get 3 split, and you got 10*3=30 small clips for each song")
parser.add_argument("k", help="number of centroids")
parser.add_argument("batchSizeRatio", help="batch size ratio when finding centroids. If there are 100 point and you specify 0.1, then batch size will be 10")
parser.add_argument("C", help="C argument for SVC Classifier")

args = parser.parse_args()
numDivide = int(args.numDivide)
k = int(args.k)
batchSizeRatio = float(args.batchSizeRatio)
C = int(args.C)

#print "--------------", "START preprocess", "--------------"
pp = preprocess.preprocess()
X, y = pp.getData("./data.in", numDivide) #path, clip numDivide

(X_center, y_center), (X_classifier, y_classifier), (X_test, y_test) = pp.splitData(
    X, y, randState=1985, TestTrainRatio=0.1, ClassifierCenterRatio=0.6)

X_center_features = pp.featureExtraction(X_center) #includes MFCC and normalization

from sklearn.cluster import MiniBatchKMeans
n, dim = X_center_features.shape
clf = MiniBatchKMeans(n_clusters=k, batch_size=int(n*batchSizeRatio), max_iter=200, max_no_improvement=None).fit(X_center_features) #X : array-like, shape = [n_samples, n_features]
centroids = clf.cluster_centers_


import vladNewVLAD as vlad
trainX_centerSubstract, trainy_centerSubstract = vlad.my_vladII(centroids, X_classifier, y_classifier)
testX_centerSubstract, testy_centerSubstract = vlad.my_vladII(centroids, X_test, y_test)

pca = PCA(n_components=128, whiten=True)
trainX_centerSubstract = pca.fit_transform(trainX_centerSubstract)
testX_centerSubstract = pca.transform(testX_centerSubstract)

from sklearn.grid_search import GridSearchCV
from sklearn import svm
import numpy as np

for c in  np.arange(0.0001, C, 0.01):
  filename = './results_svcNewVLAD200Iter_wWhitenScatterHPMFCC/{0}_{1}_{2}_{3}_svcNewVLAD200ScatterHPMFCC'.format(numDivide, k, batchSizeRatio, c)
  f = open(filename, 'w')
  svc = svm.SVC(C = c, kernel = 'linear')
  # svc = svm.LinearSVC(C=c, random_state=1985, max_iter=2000)
  svc.fit(trainX_centerSubstract, trainy_centerSubstract)
  f.write(str(svc.score(testX_centerSubstract, testy_centerSubstract)) + '\n')
  print svc.score(testX_centerSubstract, testy_centerSubstract)
  f.close()

#param_grid = {'n_neighbors': np.arange(3, 30),'weights':('uniform', 'distance'), 'algorithm':('auto','ball_tree', 'kd_tree', 'brute') }
#np.set_printoptions(suppress=True)
#grid_search = GridSearchCV(KNeighborsClassifier(), param_grid, verbose=3)
#grid_search.fit(trainX_centerSubstract, trainy_centerSubstract)

#predict = grid_search.predict(testX_centerSubstract)
#print "Predict socre:", grid_search.score(testX_centerSubstract, testy_centerSubstract)
#print "Best params:", grid_search.best_params_
