from nose.tools import *
import scipy.io
from skfeature.function.information_theoretical_based import MIFS
from sklearn import svm
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.feature_selection import SelectKBest
from sklearn.pipeline import Pipeline
from sklearn.utils import shuffle

def test_mifs():
    from sklearn.datasets import make_classification
    X, y = make_classification(n_samples=200, n_features=20, n_informative=5, n_redundant=5, n_classes=2)
    X = X.astype(float)
    n_samples, n_features = X.shape    # number of samples and number of features

    num_fea = 5

    # build pipeline
    pipeline = []
    pipeline.append(('select top k', SelectKBest(score_func=MIFS.mifs, k=num_fea)))
    pipeline.append(('linear svm', svm.LinearSVC()))
    model = Pipeline(pipeline)
    
    # split data into 10 folds
    kfold = KFold(n_splits=10, shuffle=True)
    
    results = cross_val_score(model, X, y, cv=kfold)
    print("Accuracy: {}".format(results.mean()))
    assert_true(results.mean() > 0.1)
