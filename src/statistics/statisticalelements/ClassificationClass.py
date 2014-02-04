'''
Class for a pattern classification task

Represents the statistical profile for a possible
classification within a classification task
'''

import StatisticalMeasures
from DistanceFunction import Euclid

class ClassificationClass(object):
    '''
    Class for a pattern classification task

    Represents the statistical profile for a possible
    classification within a classification task

    Attributes
    ----------
    
    
    name : str
         Name of the class
    training_samples :  array
         Representative samples for the classification
    statistical_measures :  StatisticalMeasures
         Statistical Measures of class probability distribution
    a_priori_probability : float
         A priori probability of the class 
    maximum_distance :   float
         Maximum distance between samples
    window_width : float	    
         Window width for histogram estimation 
    bandwidth : float	    
         Band width for kernel estimation 
    likelihood : float	    
         Class conditional probability, given a sample
    p_x : float
         Estimated probability for a sample in this class
	
    '''

    def __init__ (self):
        '''
        Initializes all member variables to empty values
        '''
        
        self.name = "foo"
        self.training_samples = []
        self.statistical_measures = StatisticalMeasures
        self.a_priori_probability = 0
        self.maximum_distance = 0
        self.window_width = 0        
        self.bandwidth = 0
        self.likelihood = 0
        self.p_x = 0


    def initialize (self, name, statistical_measures, 
                 training_samples, a_priori_probability, 
                 bandwidth, likelihood, p_x ):
        '''
        initializes member variables with known values

        Initializes a classificaiton with  a known 
        set of statistical characteristics and a known 
        collection of samples

        Parameters
        ----------
        name : str
           Name of the class
        training_samples :  array
           Representative samples for the classification
        statistical_measures :  StatisticalMeasures
           Statistical Measures of class probability distribution
        a_priori_probability : float
           A priori probability of the class 
        maximum_distance :   float
           Maximum distance between samples
        window_width : float	    
           Window width for histogram estimation 
        bandwidth : float	    
           Band width for kernel estimation 
        likelihood : float	    
           Class conditional probability, given a sample
        p_x : float
           Estimated probability for a sample in this class

        '''
        self.name = name
        self.statistical_measures = statistical_measures
        self.training_samples = training_samples
        self.a_priori_probability = a_priori_probability
        self.maximum_distance = 0
        self.window_width = 0
        self.bandwidth =  bandwidth 
        self.likelihood = likelihood 
        self.p_x = p_x 

        for sample_1 in training_samples:
            for sample_2 in training_samples:
                difference = Euclid.distance(sample_1, sample_2)
                if difference > self.maximum_distance:
                    maximum_distance = difference
                    window_width = maximum_distance * 0.15


    def add_sample(self, value):
        '''
        Add to training samples and recalculate stats

        Parameters
        ----------
        value : float
        '''
        self.training_samples.append(value)
