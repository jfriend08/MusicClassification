import preprocess
import cProfile

print "--------------", "START preprocess", "--------------"
pp = preprocess.preprocess()
# X, y = pp.getData("../MusicClassification/data/data_small.in", 50000) #path, clip length
X, y = pp.getData("../MusicClassification/data/data.in", 50000) #path, clip length
# X, y = pp.getData("../serverTest/MusicClassification/data/data.in", 50000) #path, clip length

(X_center, y_center), (X_classifier, y_classifier), (X_test, y_test) = pp.splitData(
    X, y, randState=1985, TestTrainRatio=0.1, ClassifierCenterRatio=0.6)

print X_center.shape, X_classifier.shape, X_test.shape

X_center_features = pp.featureExtraction(X_center) #includes MFCC and normalization
print "X_center_features.shape", X_center_features.shape #Note: this just flatten everything
print "--------------", "DONE preprocess", "--------------"


print "--------------", "START MiniBatchKMeans", "--------------"
from sklearn.cluster import MiniBatchKMeans
n, dim = X_center_features.shape
clf = MiniBatchKMeans(n_clusters=100, batch_size=int(n*0.1), max_iter=200).fit(X_center_features) #X : array-like, shape = [n_samples, n_features]
centroids = clf.cluster_centers_
print "centroids.shape", centroids.shape
print "--------------", "DONE MiniBatchKMeans", "--------------"


print "--------------", "START VLAD", "--------------"
import vlad
trainX_centerSubstract, trainy_centerSubstract = vlad.my_vlad(centroids, X_classifier, y_classifier)
testX_centerSubstract, testy_centerSubstract = vlad.my_vlad(centroids, X_test, y_test)
print trainX_centerSubstract.shape
print "--------------", "DONE VLAD", "--------------"

print "--------------", "START Grid Search", "--------------"
from sklearn.grid_search import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
import numpy as np
param_grid = {'n_neighbors': np.arange(3, 30),'weights':('uniform', 'distance'), 'algorithm':('auto','ball_tree', 'kd_tree', 'brute') }
np.set_printoptions(suppress=True)
grid_search = GridSearchCV(KNeighborsClassifier(), param_grid, verbose=3)
grid_search.fit(trainX_centerSubstract, trainy_centerSubstract)
print "--------------", "DONE Grid Search", "--------------"


predict = grid_search.predict(testX_centerSubstract)
print grid_search.score(testX_centerSubstract, testy_centerSubstract)
print grid_search.best_params_