# From: Bayesian Models for Astrophysical Data, Cambridge Univ. Press
# (c) 2017,  Joseph M. Hilbe, Rafael S. de Souza and Emille E. O. Ishida 
# 
# you are kindly asked to include the complete citation if you used this 
# material in a publication

# Code 4.5 Modifications to be applied to Code 4.3 in order 
# to use a customized likelihood

# 1 response (y) and 1 explanatory variable (x1)

import numpy as np
import statsmodels.api as sm
import pystan

from scipy.stats import uniform, norm


# create synthetic data
np.random.seed(1056)                 # set seed to replicate example
nobs= 5000                           # number of obs in model 
x1 = uniform.rvs(size=nobs)          # random uniform variable

x1.transpose()                   # create response matrix
X = sm.add_constant(x1)           # add intercept
beta = [2.0, 3.0]                # create vector of parameters

xb = np.dot(X, beta)                                  # linear predictor, xb
y = np.random.normal(loc=xb, scale=1.0, size=nobs)    # create y as adjusted
                                                      # random normal variate 

toy_data = {}                  # build data dictionary
toy_data['nobs'] = nobs        # sample size
toy_data['x'] = x1             # explanatory variable
toy_data['y'] = y              # response variable

# STAN code
stan_code = """
data {
    int<lower=0> nobs;                                 
    vector[nobs] x;                       
    vector[nobs] y;                       
}
parameters {
    real beta0;
    real beta1;                                                
    real<lower=0> sigma;               
}
model {
    vector[nobs] mu;
    real temp_const;                                   
    vector[nobs] loglike; 

    mu = beta0 + beta1 * x;                             
    
    temp_const = log(1.0/(sigma * sqrt(2 * pi())));       # multiplicative constant
    for (i in 1:nobs) {
        # loglikelihood
        loglike[i] = temp_const - pow((y[i] - mu[i]), 2) / (2 * pow(sigma, 2)); 
    }
    target += loglike;
}
"""

# fit
fit = pystan.stan(model_code=stan_code, data=toy_data, iter=5000, chains=3,
                  verbose=False)

# see results
nlines = 8                     # number of lines in screen output

output = str(fit).split('\n')
for item in output[:nlines]:
    print(item)   

