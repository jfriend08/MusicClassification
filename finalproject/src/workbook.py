import preprocess_newVLAD as preprocess
import cProfile
import argparse
from sklearn.decomposition import PCA

parser = argparse.ArgumentParser()
parser.add_argument("numDivide", help="number of split of each clip. e.g. 3 then each clip will get 3 split, and you got 10*3=30 small clips for each song")
parser.add_argument("k", help="number of centroids")
parser.add_argument("batchSizeRatio", help="batch size ratio when finding centroids. If there are 100 point and you specify 0.1, then batch size will be 10")
parser.add_argument("n_neighbors", help="n_neighbors argument for KNN Classifier")

args = parser.parse_args()
numDivide = int(args.numDivide)
k = int(args.k)
batchSizeRatio = float(args.batchSizeRatio)
n_neighbors = int(args.n_neighbors)

#print "--------------", "START preprocess", "--------------"
pp = preprocess.preprocess()
X, y = pp.getData("./data.in", numDivide) #path, clip numDivide
# X, y = pp.getData("../serverTest/MusicClassification/data/data.in", 50000) #path, clip length

(X_center, y_center), (X_classifier, y_classifier), (X_test, y_test) = pp.splitData(
    X, y, randState=1985, TestTrainRatio=0.1, ClassifierCenterRatio=0.6)

#print X_center.shape, X_classifier.shape, X_test.shape

X_center_features = pp.featureExtraction(X_center) #includes MFCC and normalization
#print "X_center_features.shape", X_center_features.shape #Note: this just flatten everything


#print "\n--------------", "START MiniBatchKMeans", "--------------"
from sklearn.cluster import MiniBatchKMeans
n, dim = X_center_features.shape
clf = MiniBatchKMeans(n_clusters=k, batch_size=int(n*batchSizeRatio), max_iter=200).fit(X_center_features) #X : array-like, shape = [n_samples, n_features]
centroids = clf.cluster_centers_
#print "centroids.shape", centroids.shape


#print "\n--------------", "START VLAD", "--------------"
import vladNewVLAD as vlad
trainX_centerSubstract, trainy_centerSubstract = vlad.my_vladII(centroids, X_classifier, y_classifier)
testX_centerSubstract, testy_centerSubstract = vlad.my_vladII(centroids, X_test, y_test)
#print trainX_centerSubstract.shape

pca = PCA(n_components=64, whiten=True)
trainX_centerSubstract = pca.fit_transform(trainX_centerSubstract)
testX_centerSubstract = pca.transform(testX_centerSubstract)

#print "\n--------------", "START Grid Search", "--------------"
from sklearn.grid_search import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
import numpy as np

for nei in  np.arange(1, n_neighbors, 1):
  filename = './results_knnNewVLADflatten/{0}_{1}_{2}_{3}_knnNewVLADflatten'.format(numDivide, k, batchSizeRatio, nei)
  f = open(filename, 'w')
  knn = KNeighborsClassifier(n_neighbors=n_neighbors, weights='uniform', algorithm='auto')
  knn.fit(trainX_centerSubstract, trainy_centerSubstract)
  f.write(str(knn.score(testX_centerSubstract, testy_centerSubstract)) + '\n')
  print knn.score(testX_centerSubstract, testy_centerSubstract)
  f.close()

#param_grid = {'n_neighbors': np.arange(3, 30),'weights':('uniform', 'distance'), 'algorithm':('auto','ball_tree', 'kd_tree', 'brute') }
#np.set_printoptions(suppress=True)
#grid_search = GridSearchCV(KNeighborsClassifier(), param_grid, verbose=3)
#grid_search.fit(trainX_centerSubstract, trainy_centerSubstract)

#predict = grid_search.predict(testX_centerSubstract)
#print "Predict socre:", grid_search.score(testX_centerSubstract, testy_centerSubstract)
#print "Best params:", grid_search.best_params_
