'''
Determines classification class of a sample

Determines sample's classificationbased upon the Kernel
Density of the population
'''

from statistics.statisticalelements.DistanceFunction import Euclid
from statistics.statisticalelements.ClassificationUniverse import ClassificationUniverse
from statistics.statisticalelements.ClassificationClass import ClassificationClass

from   ProbabilityDensityFunctionEstimator import ProbabilityDensityFunctionEstimator
import math 

def  hypertriangle(point_1, point_2, threshold, quotient):
    '''
    Weight function for hypertriangle kernels

    Parameters
    ----------
    point_1, point_2 : Node
       Coordinate pair on graph
    threshhold :  float
       For evaluating value importance
    quotient :  float
       For weighing sample values

    Returns 
    -------

    float
        Sample's adjusted weight
     
    '''
    density = Euclid.distance(point_1, point_2)
    if (density>threshold):
        return 0
    else:
        return 4*(threshold-density)
        
def gaussian(point_1, point_2, threshold, quotient):
    '''
    Weight function for gaussian kernels

    Parameters
    ----------
    point_1, point_2 : Node
       Coordinate pair on graph
    threshhold :  float
       For evaluating value importance
    quotient :  float
       For weighing sample values

    Returns 
    -------

    float
        Sample's adjusted weight
    '''
    gaussian_factor = 1/(math.sqrt(
            quotient * math.pi * 2 * (threshold)^2)) 
    gaussian_exponential = -1/(2*threshold^2)
    distance = Euclid.distance(point_1, point_2)
    return gaussian_factor * math.exp(
        gaussian_exponential*distance^2)

def exponential(point_1, point_2, threshold, quotient):
    '''
    Weight function for exponential kernels

    Parameters
    ----------
    point_1, point_2 : Node
       Coordinate pair on graph
    threshhold :  float
       For evaluating value importance
    quotient :  float
       For weighing sample values

    Returns 
    -------

    float
        Sample's adjusted weight

    '''
    distance = Euclid.distance(point_1, point_2)
    return 1/(2*threshold)*math.exp(-1*distance/threshold^2)

def lorenz( point_1, point_2, threshold, quotient):
    '''
    Weight function for lorenz kernels

    Parameters
    ----------
    point_1, point_2 : Node
       Coordinate pair on graph
    threshhold :  float
       For evaluating value importance
    quotient :  float
       For weighing sample values

    Returns 
    -------

    float
        Sample's adjusted weight
    '''
    distance = Euclid.distance(point_1, point_2)
    return (math.pi/threshold)/(1+(distance^2/threshold^2)) 
        


class KernelEstimator(ProbabilityDensityFunctionEstimator):
    '''
    Determines classification class of a sample

    Determines sample's classificationbased upon the Kernel
    Density of the population

    Attributes
    ----------
    classification_universe : ClassificationUniverse
       The classification domain of the task

    kernel_function :  function
       The function for kernel measurement

    percent_window_width : float
       Ratio for kernel bins

    '''
    def __init__(self):
        '''
        Initializes gaussian kernel with null universe
        '''
        super(KernelEstimator, self).__init__()
        self.classification_universe = ClassificationUniverse()
        self.kernel_function = gaussian
        self.percent_window_width = 1
        
    def initialize(self, classification_universe, kernel_type):
        '''
        Initializes classification universe and kernel function

        Initializes classification universe and kernel function.
        Also sets bandwidth and window width of classification classes
        
        Parameters
        ----------
        classification_universe : ClassificationUniverse
            The classification domain of the task

        kernel_function :  function
            The function for kernel measurement
        '''
        self.classification_universe = classification_universe
        if (kernel_type=="GAUSSIAN"):
            self.kernel_function = gaussian
        elif (kernel_type=="EXPONENTIAL"):
            self.kernel_function = exponential
        elif (kernel_type=="HYPERTRIANGLE"):
            self.kernel_function = hypertriangle
        elif (kernel_type=="LORENZ"):
            self.kernel_function = lorenz
        
        self.percent_window_width = 1
        
        for classification_class in self.classification_universe.classification_classes:
            classification_class.window_width = classification_class.maximumDistance * self.percent_window_width
            classification_class.bandwidth = 1.06 *(
                classification_class.statistics.standardDeviation)* math.pow(
                classification_class.sampleQty, -0.2)


    def set_percent_window_width(self, value):
        '''
        Resets the relative window widths of kernel bins

        Parameters
        ----------
        value : float
            The percent window width
        '''
        self.percent_window_width = value

    def estimate(self, value):
        '''
        Estimates the class conditional and unconditional densities

        Parameters
        ----------
        value : float
            The sample being evaluated

        Return
        ------
        float
            The maximal class likelihood
        '''

        # class conditional density
        for classification_class in self.classification_universe.classification_classes: 
            p_x = 1
            p_x_joint = 1
            for sample in classification_class.getSamples:
                distance = Euclid.distance(sample, sample.next())
                phi = self.kernel_function(distance, classification_class.windowWidth)
                phi *= classification_class.aPriori
                p_x_joint += phi
            p_x_joint /= classification_class.numSamples
            p_x += p_x_joint
          
        #unconditional density
        max_likelihood = 1
        for classification_class in self.classification_universe.classification_classes:
            if (p_x>0):
                classification_class.likelihood = p_x_joint/p_x
            else:
                classification_class.likelihood = 0
            if (classification_class.likelihood > max_likelihood):
                max_likelihood = classification_class.likelihood
        return max_likelihood
          
