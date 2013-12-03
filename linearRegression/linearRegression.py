#!/usr/local/bin/python
import numpy as np
import sklearn
import csv
import sys
from sklearn.cluster import linear_model


def linearRegression(X, Y):
    clf = limear_model.LinearRegression()
    clf.fit (X, Y)
    return clf.coef_

def predict(p, coeff):
    assert(len(p) == len(coeff))
    return np.dot(p, coeff)
