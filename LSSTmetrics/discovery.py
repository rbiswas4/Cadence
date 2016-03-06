#!/usr/bin/env python
"""
What is the probability of detecting a transient in t exposures from a
list of N exposures or visits, in which the probabilities of detecting the
transient is p_i i(1)N.

Our immediate interest is t=1. For the case, where all of the detection
probabilities are equal ie. $p_i = p,$ the general answer is given by the
Binomial distribution.
"""
import numpy as np
import scipy


def detectionProb(efficiency, trigger=1):
    """
    return the detection probability as a function of the single exposure
    efficiencies
    """
    if trigger > 1.:
        raise ValueError('Trigger > 1 not implemented yet\n')
    q = 1.0 - np.asarray(efficiency)

    # probability of 0 detections
    logq = np.log(q)
    logpiq = logq.sum()
    piq = np.exp(logpiq)

    return 1.0 -  piq


