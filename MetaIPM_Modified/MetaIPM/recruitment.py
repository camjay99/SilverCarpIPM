import numpy as np

class Ricker_recruitment:
    '''
    Defines a Ricker recruitment function.

    Adapted from Punt and Methot's
    The Impact of Recruitment Projection Methods
    on Forecasts of Rebuilding Rates for
    Overfished Marine Resources
    '''
    def __init__(self, R0, S0, h):
        self.R0 = R0
        self.S0 = S0
        self.h = h

    def __call__(self, SSB):
        out = ((SSB / (self.S0 / self.R0))) * \
            ((5.0 * self.h) ** (5.0 / 4.0)) ** \
            (1.0 - (SSB / self.S0))
        return out


class Beverton_Holt_recruitment:
    '''
    Defines a Beverton-Holt recruitment function.
    '''
    def __init__(self, R0, S0, h):
        self.R0 = R0
        self.S0 = S0
        self.h = h

    def __call__(self, SSB):
        out = ((SSB/self.S0) * self.R0) / \
            (1.0 - (((5.0 * self.h)/4 * self.h) *
                    (1 - SSB / self.S0)))
        return out

class Logistic_recruitment:
    '''
    Defines a logistic recruitment function based on
    size.
    '''
    def __init__(self, alpha, beta, min_recruit, max_recruit):
        self.alpha = alpha
        self.beta = beta
        self.min_recruit = min_recruit
        self.max_recruit = max_recruit
        
    def __call__(self, z):
        out = self.min_recruit + \
            ((self.max_recruit - self.min_recruit) / \
             (1 + np.exp(-self.beta*(z - self.alpha))))
        return out