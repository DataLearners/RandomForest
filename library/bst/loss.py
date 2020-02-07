# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 14:48:14 2019

@author: Douglas Brown

Module contains the loss function(s) to be optimized for the algorithm
"""
import statistics
import prep
from bst import config

class Score:
    """Store the loss function score of the node"""
    def __init__(self, settings, data, resp_col):
        self.settings = settings
        self.data = data
        self.resp = resp_col
        self.weight = len(data)/settings.N
        self.value = score_node(data, resp_col, settings.loss_func)

def gini(data, resp_col):
    """Calculate the Gini Impurity for a list of rows"""
    counts = prep.class_counts(data, resp_col)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / len(data)
        impurity -= prob_of_lbl**2
    return impurity

def gini_wgtd(left, right, resp_col):
    """Weighted Gini impurity based on size of child nodes"""
    p_p = float(len(left)) / (len(left) + len(right))
    g_left = gini(left, resp_col)
    g_right = gini(right, resp_col)
    return p_p * g_left + (1 - p_p) * g_right


def var(data, resp_col):
    y_stat = [row[resp_col] for row in data]
    if len(y_stat) > 1:
        return statistics.variance(y_stat)
    else:
        return 0

def var_wgtd(left, right, resp_col):
    """Weighted sum of squared residuals based on size of child nodes"""
    p_p = len(left) / (len(left) + len(right))
    g_left = var(left, resp_col)
    g_right = var(right, resp_col)
    return p_p * g_left + (1 - p_p) * g_right

def score_node(data, resp_col, loss):
    if loss == 'gini':
        return gini(data, resp_col)
    elif loss == 'var':
        return var(data, resp_col)

def info_gain(true_data, false_data, resp_col, loss):
    if loss == 'gini':
        return gini_wgtd(true_data, false_data, resp_col)
    elif loss == 'var':
        return var_wgtd(true_data, false_data, resp_col) 

