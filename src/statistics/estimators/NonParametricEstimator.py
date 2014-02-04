'''
Estimates the class membership of a given sample

The Non Parametric Probability Density Estimator
combines a histogram estimator and a kernel estimator
to build a non parametric estimation model
'''

from HistogramEstimator  import  HistogramEstimator, Histogram
from statistics.statisticalelements.ClassificationClass import ClassificationClass
from statistics.statisticalelements.ClassificationUniverse import   ClassificationUniverse
from KernelEstimator import KernelEstimator

class   NonParametricProbabilityDensityEstimator(object):
    '''
    Estimates the class membership of a given sample

    The Non Parametric Probability Density Estimator
    combines a histogram estimator and a kernel estimator
    to build a non parametric estimation model

    Attributes
    ----------
    kernel_estimator : KernelEstimator
       For estimating sample's class membership
    histogram_estimator : HistogramEstimator
       For estimating sample's class membership
    classification_class : ClassificationClass
       The class whose likelihood is being estimated
    classification_universe : ClassificationUniverse
       The entire domain of classification 
    maximum_distance : float
       Maxiumum possible distance between samples
    '''
    def __init__(self):
        '''
        Initializes all member variables to null values
        '''
        self.classification_class = ClassificationClass()
        self.classification_universe = ClassificationUniverse()
        self.kernel_estimator = KernelEstimator()
        self.histogram_estimator = HistogramEstimator()
        self.maximum_distance = 0

    def initialize_classification (self, classification_class, classification_universe):
        '''
        Initializes classification class and universe

        Parameters
        ----------

        classification_class : ClassificationClass
            The class whose likelihood is being estimated
        classification_universe : ClassificationUniverse
            The entire domain of classification 
        '''
        self.classification_class = classification_class
        self.classification_universe = classification_universe

    def set_maximum_distance(self, value):
        '''
        Sets the maximum possible distance between samples
        Parameters
        ----------
        value : float
            The maximum window width
        '''
        self.maximum_distance = value

    def estimate(self, value, is_sample_new=False):
        '''
        Estimates the class membership of a given value

        Parameters
        ----------
        value : float
            Value of sample

        Returns
        -------
        int
            Classification Class ID
        '''

        if (self.histogram_estimator):
            return self.histogram_estimator.estimate(value)
        else :
            if (is_sample_new):
                value = self.recalculate_statistics()
            self.kernel_estimator.set_percent_window_width(value)
            return self.kernel_estimator.estimate(value)

    def recalculate_statistics(self):
        '''
        Reinitializes global stats of classification domain
        '''
        self.classification_universe = ClassificationUniverse()
        self.classification_universe.add_classification_class(self.classification_class)
        self.kernel_estimator.initialize(self.classification_universe, "GAUSSIAN")


    def add_sample(self, value):
        '''
        Adds a sample to the classification class

        Parameters
        ----------
        value : float
            Value being added to class
        '''
        
        self.classification_class.add_sample(value)

    def convert_to_histogram(self, bins, do_average_shift):
        '''
        Represents the estimation by using a Histogram

        Parameters
        ----------
        bins : Array of HistogramBins
            Bins that constitute the Histogram
        do_average_shift : boolean
            Whether to make an Average Shifted Histogram
        '''
        histogram = Histogram(bins)
        if (do_average_shift):
            histogram.make_average_shifted_histogram()
        self.histogram_estimator = HistogramEstimator(histogram)
