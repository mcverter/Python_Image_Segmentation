'''
The Boykov Framework inherits from the GraphCutFrameowork
The Boykov_Framework coordinates together
(1)  The pixel intensity observations taken from the original image
(2) The object seeds given at startup
(3) The background seeds given at startup
(4) The estimation model for the source region
(5) The estimation model for the sink region
(6) The estimation model for the boundary between these two regions
'''

from GraphCutFramework import GraphCutFramework
import math

class BoykovFramework(GraphCutFramework):
    '''
    The Boykov Framework inherits from the GraphCutFrameowork
    The Boykov_Framework coordinates together
    (1)  The pixel intensity observations taken from the original image
    (2) The object seeds given at startup
    (3) The background seeds given at startup
    (4) The estimation model for the source region
    (5) The estimation model for the sink region
    (6) The estimation model for the boundary between these two regions
    

    The processing done by this framework is fed into the 
    Boykov-Kolmogorov Graph Cut Energy Minimization algorithm  
    in order to delineate target segments from non-target segments.


    The BoykovFramework is differentiated from the MAP_CRF _Framework in the following ways:
    (1) Differing ways of calculating the neighbor-edge weight
    (2) The Boykov Framework makes use of the boykov_sigma
    (3) The MAP_CRF_Framework makes use of a Conditional Random Field recalculation of the Maximum A Priori.  
   

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


    def __init__(self, image_interface, estimator, crf_lambda, boykov_sigma):
        '''
        Initializes all member variables
        '''
        super(BoykovFramework, self).__init__(image_interface, estimator, crf_lambda)
        self.boykov_sigma = boykov_sigma
        

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
        max_neighbor_link_cost = 1
        observed_1 = self.image_interface.get_observation(x_1, y_1)
        observed_2 = self.image_interface.get_observation(x_2, y_2)
        
        difference = (observed_1-observed_2)^2
        distance = self.image_interface.get_observation(x_1, y_1, x_2, y_2)
        forward_weight = math.exp(-difference/(2*self.boykov_sigma^2))/distance
        backward_weight = forward_weight
        if (backward_weight > max_neighbor_link_cost):
            max_neighbor_link_cost = backward_weight  
        return [forward_weight, backward_weight]


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

        neighbors = self.image_interface.get_neighbor_nodes(xxx, yyy)
        node_feature = self.image_interface.get_observation(xxx, yyy)
        max_neighbor_link_cost = 1
        
        for neighbor in neighbors:
            neighbor_feature = self.image_interface.get_observation(
                neighbor.x, neighbor.y)
            difference = (neighbor_feature-node_feature)^2
            distance = self.image_interface.get_distance(node, neighbor)
            forward_weight = math.exp(-difference/(2*self.boykov_sigma^2))/distance
            forward_weight *= self.crf_lambda
            backward_weight = forward_weight
            if (backward_weight > max_neighbor_link_cost):
                max_neighbor_link_cost = backward_weight
        return [forward_weight, backward_weight]
    
