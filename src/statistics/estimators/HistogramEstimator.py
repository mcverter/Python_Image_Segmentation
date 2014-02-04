'''
Estimates the classification class membership of a given value
'''

from  ProbabilityDensityFunctionEstimator import ProbabilityDensityFunctionEstimator


class HistogramBin(object):
    '''
    A bin for placing samples in.


    Attributes
    ----------
    
    width : float
        The size of the bin
    qty :  int
        Number of elements in bin
    weight : float
        Total weight contained in the bin
        (Different elements may have different weights)

    '''
    def __init__ (self):
        '''
        Initializes the member variables to null values
        '''
        self.width = 0
        self.qty = 0
        self.weight = 0



class Histogram(object):
    '''
    Models the probability distribution of a classification.

    Attributes
    ----------
    hist_bins : array of HistogramBin
        The bins contained within the model
    total_elements : int
        Total number of elements in Histogram
    total_weight : float
        Total weight of elements in histogram
    '''

    def __init__ (self, hist_bins):
        '''
        Initializes member variables to null values
        '''
        self.hist_bins = []
        self.total_elements = 0
        self.total_weight = 0

    def add_bins(self, hist_bins):
        '''
        Adds a set of bins to the histogram

        Appends the new bins and recalculates the
        total_elements and total_weight.

        Parameters
        ----------

        hist_bins : array of HistogramBin
            Bins being added to the Histogram
        '''
        self.hist_bins.append(hist_bins)
        for histbin_bin in hist_bins:
            self.total_elements += histbin_bin.qty
            self.total_weight += histbin_bin.weight
        
    def add_element(self, index, weight):
        '''
        Adds a weighted element to the histogram at the given index

        Parameters
        ----------

        index : int
            Index of the bin
        weight : float
            Weight of the element

        '''
        hist_bin = self.hist_bins[index]
        hist_bin.weight += weight
        hist_bin.qty += 1
        self.total_weight += weight
        self.total_elements += 1

    def make_average_shifted_histogram(self):
        ''' 
        Converts the raw histogram to an Average Shifted Histogram

        Returns
        -------
        Histogram
           A Histogram which has been shifted to fit the data
        '''
        ash = Histogram()
        for hist_bin in self.hist_bins:
            # shift_over_the_bins
            1
        return ash



class HistogramEstimator(ProbabilityDensityFunctionEstimator) :
    '''
    Estimates the classification class membership of a given value

    Attributes
    ----------

    histogram : Histogram
        Stores the samples
    '''
    def __init__(self):
        '''
        Initializes histogram to null
        '''
        super(HistogramEstimator, self).__init__()
        self.histogram = Histogram()


    def estimate(self, value):
        '''
        Estimates the class membership of a given value

        Parameters
        ----------
        value : float
            Value of sample

   
        int
            Classification Class ID
        '''
        return 1
