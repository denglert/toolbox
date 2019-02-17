#!/usr/bin/env python

import numpy as np
import scipy.stats
import matplotlib.pyplot as plt


#######################
### --- Poisson --- ###
#######################


def poisson_two_sided(n_obs, alpha=0.05): 
    """
    Calculates the two-sided, symmetric confidence interval with α significance level.
    """

    lambda_CI_LL = 0.5 * scipy.stats.chi2.ppf(    alpha/2.0, 2*(n_obs))
    lambda_CI_UL = 0.5 * scipy.stats.chi2.ppf(1.0-alpha/2.0, 2*(n_obs+1))

    return lambda_CI_LL, lambda_CI_UL


def poisson_upper(n_obs, alpha=0.05):
    """Calculates the one-sided, upper bound confidence interval with α significance level"""

    chi2_df = 2 * (n_obs+1)
    lambda_UL = 0.5 * scipy.stats.chi2.ppf(1.0-alpha, df=chi2_df)
    return lambda_UL


def poisson_upper_CLs(n_obs, bkg, alpha=0.05):

    pb = 1.0 - scipy.stats.poisson.cdf(n_obs, mu=bkg)
    chi2_df = 2 * (n_obs+1)
    alpha_corrected = alpha*(1.0-pb)
    lambda_UL = 0.5 * scipy.stats.chi2.ppf(1.0-alpha_corrected, df=chi2_df)

    return lambda_UL
