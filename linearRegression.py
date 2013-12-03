#!/usr/local/bin/python
import numpy as np
import sklearn
import csv
import sys
from sklearn import linear_model


def linearRegression(X, Y):
    clf = linear_model.LinearRegression()
    clf.fit (X, Y)
    return clf
