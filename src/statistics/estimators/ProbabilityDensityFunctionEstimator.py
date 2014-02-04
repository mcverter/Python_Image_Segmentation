'''
Abstract class for statistical estimation
'''

class ProbabilityDensityFunctionEstimator(object):
    '''
    Abstract class for statistical estimation
    '''
    def __init__(self):
        '''
        Initializes class
        '''
        return

    def estimate(self, value):
        '''
        Parameters
        ----------
        
        value : float
            value of a sample


        Raises
        ------
        NotImplementedError
            Function must be called from inherited class
        '''
        raise NotImplementedError("You must run this from an inherited class")
    
