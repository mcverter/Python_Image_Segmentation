''' 
Statistical descriptions of probability distribution

A container for the the various measures of 
statistical probability distribution of the various
Classification Classes as well as the Classification
Universe as a whole
'''

class StatisticalMeasures(object):
    ''' 
    Statistical descriptions of probability distribution

    A container for the the various measures of 
    statistical probability distribution of the various
    Classification Classes as well as the Classification
    Universe as a whole

    Attributes
    ----------
    
    minimum : float
         Minimum possible value for a sample
    maximum :  float
         Maximum possible value for a sample
    mean :  float
         Average value of a sample
    standard_deviation :  float
         Standard deviation of samples
    variance :  float
         Standard deviation of samples

    '''
    def __init__(self, minimum, maximum, mean, standard_deviation, variance):
        self.minimum = minimum
        self.maximum = maximum
        self.mean = mean
        self.standard_deviation = standard_deviation
        self.variance = variance
        

