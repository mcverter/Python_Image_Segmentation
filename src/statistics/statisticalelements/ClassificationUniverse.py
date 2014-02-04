''' 
Entire Classification Region 

The Classification Univerese is used  to coordinate 
the various classification classes in a 
classification task.
'''

from ClassificationClass import ClassificationClass
from StatisticalMeasures import StatisticalMeasures
from DistanceFunction import Euclid
from math import sqrt

class ClassificationUniverse(object):
    ''' 
    Entire Classification Region 

    The Classification Univerese is used  to coordinate 
    the various classification classes in a 
    classification task.
    
    Attributes
    ----------
    
    (1) name : str
           Name of the universe 
    (2) classification_classes:  array 
           Collection of classification classes
    (3) total_samples_qty : int	
           Total number of samples for all classes
    (4) global_statistical_measures : StatisticalMeasures
           Global statistical measures of probability
    (5) distance_function : function		
           Function for determining distance between samples 
    '''
    def __init__(self, name="foo", distance_function=Euclid ):
        '''
        initializes member variables to empty values

        Parameters
        ----------

        name : str
           Name of the class
        distance_function : function
           Function for determining distance between samples 
        '''

        self.name = name
        self.total_samples_qty = 0
        self.global_statistical_measures = StatisticalMeasures(0, 0, 0, 0, 0)

        self.classification_classes = []
        self.distance_function = distance_function

    def add_classification_class(self, classification_class):
        '''
        Adds classification class and recalculates global stats 

        Parameters
        ----------

        classification_class : ClassificationClass
           Added class
        '''
        self.classification_classes.append(classification_class)
        self.update_global_statistics(classification_class)

    def update_global_statistics (self, classification_class ):
        '''
        Recalculates global statistics 

        When a new class is added, the global statistical
        model must be recomputed

        Parameters
        ----------

        classification_class : ClassificationClass
           Added class
        '''
        class_stats = classification_class.statistical_measures
        global_stats = self.global_statistical_measures

        if class_stats.minimum < global_stats.minimum:
            global_stats.minimum = class_stats.minimum
        if class_stats.maximum < global_stats.minimum:
            global_stats.maximum = class_stats.maximum

        class_samples = classification_class.training_samples

        class_sample_qty = classification_class.training_samples.length
        self.total_samples_qty = class_sample_qty



        for sample in class_samples:
            difference = Euclid.distance(sample, global_stats.mean)
            global_stats.variance += difference^2
            global_stats.standard_deviation += sqrt(global_stats.variance/class_sample_qty -1)
        class_stats.maximum = global_stats.maximum
        class_stats.minimum = global_stats.minimum

        class_stats.standard_deviation = global_stats.standard_deviation
        class_stats.variance = global_stats.variance

        
        global_sample = global_stats.mean
        maximum_distance = 0
        for local_sample in class_samples:
            difference = Euclid.distance (global_sample, local_sample)
            if difference > maximum_distance:
                maximum_distance = difference

        window_width = 0.15 * maximum_distance
        
