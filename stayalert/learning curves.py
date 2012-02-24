#!/usr/bin/env python
# encoding: utf-8
"""
learning curves.py

Created by Harit Himanshu on 2012-02-23.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

"""Plot error curves for various dataset sizes

This plot emphasizes the lack of data: by following the trend, one
can expect test score to further increase and help reduce the overfit.

Further more as the train error seems to remain pretty close to the perfect
score when the dataset size grows one can estimate that the model does not
underfit too much (is not too simplistic / biased).
"""
import numpy as np
from time import time

from sklearn.cross_validation import ShuffleSplit
from sklearn.datasets import fetch_20newsgroups_vectorized
from sklearn.naive_bayes import MultinomialNB
from sklearn.base import clone
from StringIO import StringIO
from sklearn.linear_model.logistic import LogisticRegression
from sklearn import linear_model


def score_curves(clf_orig, X, y, n_runs=5, test_fraction=0.1,
                 train_fraction_range=np.linspace(0.1, 0.9, 10)):

    n_datasets = train_fraction_range.shape[0]
    training_score = np.zeros((n_datasets, n_runs))
    test_score = np.zeros((n_datasets, n_runs))
    training_time = np.zeros((n_datasets, n_runs))

    for i, train_fraction in enumerate(train_fraction_range):
        print "Train fraction: %0.2f" % train_fraction

        cv = ShuffleSplit(n_samples, n_iterations=n_runs,
                          test_fraction=test_fraction,
                          train_fraction=train_fraction)
        for j, (train, test) in enumerate(cv):
            clf = clone(clf_orig)
            t0 = time()
            clf.fit(X[train], y[train])
            training_time[i, j] = time() - t0
            training_score[i, j] = clf.score(X[train], y[train])
            test_score[i, j] = clf.score(X[test], y[test])

    return training_score, test_score, training_time


if __name__ == "__main__":
    # data = fetch_20newsgroups_vectorized(subset='all')
    #     categories = data.target_names
    #     X = data.data
    #     y = data.target
    #     n_samples = y.shape[0]
    #     n_features = X.shape[1]
    f = open('/Users/hhimanshu/Downloads/data/fordTrain.csv', 'r')
    data = np.genfromtxt(StringIO(f.read()), delimiter=',')
    f = open('/Users/hhimanshu/Downloads/data/fordTrain.csv', 'r')
    data = np.genfromtxt(StringIO(f.read()), delimiter=',')
    data_header_stripped = data[1:,:]
    data_header_stripped = np.roll(data_header_stripped, -3, axis=1) # rolling 3 column of labels to last column
    X = data_header_stripped[:, 0:-1]
    y = data_header_stripped[:, -1]
    n_samples = y.shape[0]
    n_features = X.shape[1]
    #print data
    #print y.shape
    print "n_samples: %d, n_features: %d" % (n_samples, n_features)

    #clf = MultinomialNB(alpha=.01)
    #clf = LogisticRegression(C=1.9, penalty='l2')
    clf = linear_model.SGDClassifier()
    train_fraction_range = np.linspace(0.1, 0.9, 5)
    test_fraction = 0.1

    train_score, test_score, training_time = score_curves(
        clf, X, y, train_fraction_range=train_fraction_range,
        test_fraction=test_fraction)

    print clf
    mean_test_score = test_score.mean(axis=1)
    mean_train_score = train_score.mean(axis=1)
    gap = np.abs(mean_test_score - mean_train_score)
    print "Best test score: %0.2f" % mean_test_score.max()
    print "Gap at train_fraction=%0.2f: %0.2f" % (
        train_fraction_range[-1], gap[-1])

    import pylab as pl
    plots = []
    plots.append(pl.errorbar(train_fraction_range,
                             mean_train_score,
                             train_score.std(axis=1)))
    plots.append(pl.errorbar(train_fraction_range,
                             mean_test_score,
                             test_score.std(axis=1)))

    pl.legend(plots, ('train', 'test'), loc='lower right')

    pl.title("Learning curves for %r\n"
             "Best test score: %0.2f - Gap: %0.2f" %
             (clf, mean_test_score.max(), gap[-1]))
    pl.ylim(0.0, 1.0)
    pl.ylabel('Classification score')
    pl.xlabel('Fraction of the dataset used for training\n'
              'The test fraction is fixed to %0.2f' % test_fraction)
    pl.show()
