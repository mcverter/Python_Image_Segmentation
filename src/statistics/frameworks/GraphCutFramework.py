'''
A GraphCutFramework coordinates together
(1)  The pixel intensity observations taken from the original image
(2) The object seeds given at startup
(3) The background seeds given at startup
(4) The estimation model for the source region
(5) The estimation model for the sink region
(6) The estimation model for the boundary between these two regions
'''

from image_definition.ImageSlice import ImageInterface
from statistics.estimators.MapCrfEstimator import MapCrfEstimator
import math

FLOW_EPSILON = 1

class GraphCutFramework(object):
    '''
    A GraphCutFramework coordinates together
    (1)  The pixel intensity observations taken from the original image
    (2) The object seeds given at startup
    (3) The background seeds given at startup
    (4) The estimation model for the source region
    (5) The estimation model for the sink region
    (6) The estimation model for the boundary between these two regions
    

    The processing done by this framework is fed into the 
    Boykov-Kolmogorov Graph Cut Energy Minimization algorithm  
    in order to delineate target segments from non-target segments.

    The GraphCutFraumework is an abstract class and should never be instantiated as an object
    Instead, one should use the MAP_CRF_Framework or the BoykovFramework


    Attributes
    ----------
    image_interface : ImageInterface
        Supplies the intensities of the pixels as well as 
        the locations of source and sink nodes
    estimator : MapCrfEstimator
        Estimator for sink, source, and boundary
    crf_lambda : float
        Constant for usage in CRF calculations
    max_nbr_link_cost : float
        Threshold for neighbor links
    do_boundary_only : bool
        Whether only to train the boundary
    '''

    def __init__ (self, image_interface, estimator, crf_lambda):
        '''
        Initializes all member variables
        '''
        self.image_interface = image_interface
        self.estimator = estimator
        self.crf_lambda = crf_lambda
        self.do_boundary_only = False
        self.max_nbr_link_cost = 1
        self.initialize (image_interface, estimator, crf_lambda)








    def get_neighbor_link_cost(self, xxx, yyy):
        '''
        Returns the cost of the neighbor link
        
        Parameters
        ----------
        xxx, yyy : int
            Indexes of the node

        Returns
        -------
        float 
            Cost of link

        Raises
        -----
        NotImplementedError
              This is an abstract method which must 
              be implemented by subclasses
        '''
        raise NotImplementedError( "Graph Cut Framework is an abstract base class.  Please use MAP_CRF_Framework or BoykovFramework")

    def get_n_link_cost(self, x_1, y_1, x_2, y_2):
        ''' 
        Returns the neighbor link between two nodes
        
        Parameters
        ----------
        x_1, y_1, x_2, y_2 : int
            Indexes of the two nodes

        Returns
        -------
        float 
            Cost of link between the nodes

        Raises
        -----
        NotImplementedError
              This is an abstract method which must 
              be implemented by subclasses
        '''
        raise NotImplementedError( "Graph Cut Framework is an abstract base class.  Please use MAP_CRF_Framework or BoykovFramework")




    def get_st_link_cost(self, xxx, yyy):
        '''
        Gets the cost between the node and the source and sink

        Parameters
        ----------
        xxx, yyy : int
            Indexes of the node

        Returns
        -------
        int 
            Cost of link to source
        int 
            Cost of link to sink
        '''
        max_nbr_link_cost = 1  
        if (self.image_interface.is_object_seed(xxx, yyy)):
            seed_value = max_nbr_link_cost+1
            sink_value = 0

        elif (self.image_interface.is_background_seed(xxx, yyy)):
            sink_value = max_nbr_link_cost+1
            seed_value = 0
        else:   
            if (self.do_boundary_only==False):
                observation = self.image_interface.get_observation(xxx, yyy)
                source_value = self.estimator.estimate_source_region(observation)
                sink_value = self.estimator.estimate_sink_region(observation)
            else:
                source_value = 0.5
                sink_value = 0.5
            if (source_value < FLOW_EPSILON):
                source_value = FLOW_EPSILON

            if (sink_value < FLOW_EPSILON):
                sink_value = FLOW_EPSILON
        
            sink_value = -math.log(sink_value)
            source_value = -math.log(source_value)
        return [source_value, sink_value]

    def get_neighbor_nodes(self, xxx, yyy):
        '''
        Gets the neighboring nodes to a node

        Parameters
        ----------
        xxx, yyy : int
            Indexes of the node

        Returns
        -------
        list:
            List of Neighboring Nodes
        '''
        return self.image_interface.get_neighbor_pixels(xxx, yyy)

    def get_update_st_link_costs(self):
        '''
        Updates the links between all the nodes and the source and sink
        '''
        node_list = []
        object_seeds = self.image_interface.get_new_object_seeds()
        background_seeds = self.image_interface.get_new_background_seeds()


        for seed in object_seeds:
            node_list.add_object_seed(seed)
            sourceCostList.add(max_neighbor_link_cost+1)
            sinkCostList.add(0)

        for seed in background_seeds:
            nodeList.addBackgroundSeed(seed)
            sinkCostList.add(max_neighbor_link_cost+1)
            sourceCostList.add(0)
  

