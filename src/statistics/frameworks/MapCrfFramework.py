'''
The MAP_CRF_Framework coordinates together
(1)  The pixel intensity observations taken from the original image
(2) The object seeds given at startup
(3) The background seeds given at startup
(4) The estimation model for the source region
(5) The estimation model for the sink region
(6) The estimation model for the boundary between these two regions
'''

from GraphCutFramework import GraphCutFramework, FLOW_EPSILON
import math

class MapCrfFramework (GraphCutFramework):
    '''
    The MAP_CRF_Framework coordinates together
    (1)  The pixel intensity observations taken from the original image
    (2) The object seeds given at startup
    (3) The background seeds given at startup
    (4) The estimation model for the source region
    (5) The estimation model for the sink region
    (6) The estimation model for the boundary between these two regions
    

    The processing done by this framework is fed into the 
    Boykov-Kolmogorov Graph Cut Energy Minimization algorithm  
    in order to delineate target segments from non-target segments.

    The  MAP_CRF_Framework is differentiated from the BoykovFramework in the following ways:
    (1) Differing ways of calculating the neighbor-edge weight
    (2) The MAP_CRF_Framework makes use of a Conditional Random Field recalculation of the Maximum A Priori. 
    (3) The Boykov Framework makes use of the boykov_sigma


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
    boykov_sigma :  float
        Constant for usage in link weight calculations
 
    '''

    def __init__(self, image_interface, estimator, crf_lambda):
        '''
        Initializes all member variables
        '''
        super(MapCrfFramework, self).__init__(image_interface, estimator, crf_lambda)


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
        '''
        neighbors = self.image_interface.get_neighbor_pixels(xxx, yyy)
        node_feature = self.image_interface.get_observation(xxx, yyy)
        max_neighbor_flow_cost = 1
        for neighbor in neighbors:
            neighbor_feature = self.image_interface.get_observation(xxx, yyy)
            boundary_forward = self.estimator.get_boundary(node_feature, neighbor_feature)
            boundary_backward = self.estimator.get_boundary(neighbor_feature, node_feature)
            if (boundary_forward < FLOW_EPSILON):
                boundary_forward = FLOW_EPSILON
            if (boundary_backward < FLOW_EPSILON):
                boundary_backward = FLOW_EPSILON
            
            log_forward = -math.log(boundary_forward) * self.crf_lambda
            if log_forward > max_neighbor_flow_cost:
                max_neighbor_flow_cost = log_forward

            log_backward = -math.log(boundary_backward) * self.crf_lambda
            if log_backward > max_neighbor_flow_cost:
                max_neighbor_flow_cost = log_backward
                
        return [log_forward, log_backward]

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
        '''
        return 1





