''' 
This is the main driver class for the graph cut program.  

It takes in a raw ImageSlice and markings of the object
and the background regions.

From these inputs, it outputs a fully segmented image.
'''



import numpy as np
import scipy as sp
from pylab import imread
from statistics.frameworks.BoykovFramework import BoykovFramework
from statistics.frameworks.MapCrfFramework import MapCrfFramework
from statistics.estimators.HistogramEstimator import  HistogramEstimator
from statistics.estimators.KernelEstimator import KernelEstimator  
from statistics.estimators.MapCrfEstimator import MapCrfEstimator
from statistics.estimators.NonParametricEstimator import NonParametricProbabilityDensityEstimator
from image_definition.ImageSlice import ImageInterface
from image_definition.ImageCreator import ImageCreator
from STCut import STCut

class PerformGraphCut(object):
    ''' 
    This is the main driver class for the graph cut program.  

    It takes in a raw ImageSlice and markings of the object
    and the background regions.
    
    From these inputs, it outputs a fully segmented image.


    Attributes
    ----------

    crf_lambda : float
        Constant for CRF calculations
    sigma : float
        Constant for Boykov calculations
    bin_qty :  int
        Constant for histogram estimation
    bin_size :  int
        Constant for histogram estimatio
    do_only_boundary : bool
        Only train boundary
    do_regional_training : bool
        Train regional estimators
    do_boundary_training : bool
        Train boundary estimators
    object_seeds : list
        Array of object seeds
    background_seeds : list
        Array of background seeds
    image_interface : ImageInterface 
        Provider of pixel intensity information
    framework :  GraphCutFramework
        Coordinates the image with the regional estimators
    segmentation : STCut
        Executes the graph cut algorithm
    '''

    def __init__(self):
        '''
        Initializes member variables
        '''

        # initial global variables
        self.crf_lambda = 1
        self.sigma = 1
        self.do_only_boundary = False
        self.bin_qty = 1
        self.bin_size = 1
        self.do_boundary_training = True
        self.do_regional_training = True
        self.object_seeds = []
        self.background_seeds = []
        self.framework = None
        self.segmentation = None
        self.image_interface

    def perform_cut(self, img_file, object_file, background_file):
        '''
        This function produces a regionally segmented image

        It takes in a raw ImageSlice and markings of 
        the object and the background regions.
    
        From these inputs, it outputs a fully 
        segmented image.
        '''
        

        # initialize images
        image = imread(img_file)
        self.object_seeds = imread(object_file)
        self.background_seeds = imread(background_file)
        self.image_interface = ImageInterface(image)
        #initialize_image_object
        #set_image_object_pixels()

        #initialize trainers
        trainer_source = MapCrfEstimator()
        trainer_sink = MapCrfEstimator()

        #initialize estimators
        estimator_boundary = NonParametricProbabilityDensityEstimator()
        estimator_sink  = NonParametricProbabilityDensityEstimator()
        estimator_source  = NonParametricProbabilityDensityEstimator()

        # process object seeds 
        for seed in self.object_seeds:
            xxx = seed.x
            yyy = seed.y
            intensity = self.image_interface.get_observation(xxx, yyy)
            estimator_source.add_sample(intensity)
            self.image_interface.add_object_seed(xxx, yyy)

        #process background seeds
        for seed in self.background_seeds:
            xxx = seed.x
            yyy = seed.y
            estimator_sink.add_sample(intensity)
            self.image_interface.add_background_seed(xxx, yyy)
        
       # prepare background training
        if (self.do_regional_training):
            global_object_samples = []
            global_background_samples = []
            for intensity in global_object_samples:
                estimator_source.add_sample(intensity)

            for intensity in global_background_samples:
                estimator_source.add_sample(intensity)

                
        # Build histograms for Estimators
        estimator_source.convert_to_histogram(1, True)
        estimator_sink.convert_to_histogram(1, True)
        estimator_source.set_maximum_distance(100)
        estimator_sink.set_maximum_distance(1000)

        # prepare training estimators
        trainer_source.set_source_estimator(estimator_source)
        trainer_sink.set_sink_estimator(estimator_sink)

        boundary_samples = []
        # boundary estimator
        for sample in boundary_samples:
            estimator_boundary.add_sample(sample)
        estimator_boundary.convert_to_histogram(1, True)

        map_estimator = MapCrfEstimator(estimator_source, estimator_sink, estimator_boundary) 

        trainer_background = None
        if (self.do_boundary_training == True):
            self.framework = MapCrfFramework((self.image_interface, map_estimator, trainer_source, trainer_sink, trainer_background, self.crf_lambda))
        else:
            self.framework = BoykovFramework((self.image_interface, map_estimator, self.crf_lambda, self.sigma))
        
        self.segmentation = STCut(self.framework)
        partition = self.segmentation.execute_cut()

        # create output images
        image_creator = ImageCreator()
        image_creator.construct_image(partition)


 
