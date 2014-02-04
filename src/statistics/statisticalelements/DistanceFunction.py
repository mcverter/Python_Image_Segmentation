'''
Measures distance between two nodes.

This class is being used to hold the various 
Distance Functions that can be used to measure the
distance between classification samples

'''

from math import sqrt

class DistanceFunction(object):
    '''
    Measures distance between two nodes.

    This class is being used to hold the various 
    Distance Functions that can be used to measure the
    distance between classification samples

    '''
    def __init__(self):
        '''
        Abstract class initialization

        An abstract method that should be implemented by subclasses
        '''
        return

    
    def  distance (self, node_1, node_2):
        '''
        Finds distance between two nodes

        Abstract method that should be implemented by subclasses

        Parameters
        ----------
        node_1, node_2 : Node
           Graph Nodes
        
        Raises
        ------
        NotImplementedError
           Should only be called from a subclass
        '''
        raise NotImplementedError("This is an abstract class.")


class Euclid (DistanceFunction):
    '''
    This class models the Euclidian distance
    '''

    def __init__(self):
        '''
        Initializes the class
        '''
        super.__init__()
        return

    def distance (self, node_1, node_2):
        '''
        Finds Euclidian distance between two nodes

        Parameters
        ----------
        node_1, node_2 : Node
           Graph Nodes
      

        Returns
        -------
        float
            Distance between nodes

        Notes
        -----
        Currently  implemented only in 2D


        '''
        return sqrt((node_1.x - node_2.x)^2 +
                    (node_1.y - node_2.y)^2)
    
class Chebychev (DistanceFunction):
    '''
    This models the Chebychev distance.  
    
    Notes
    -----
    Currently this is just a placeholder
    '''

    def __init__(self):
        '''
        Initializes the class
        '''
        super.__init__()
        return

    def distance (self, node_1, node_2):
        '''
        Finds Chebychev distance between two nodes

        Parameters
        ----------
        node_1, node_2 : Node
           Graph Nodes
      

        Returns
        -------
        float
            Distance between nodes

        Notes
        -----
        Currently implemented only in 2D
        Currently just a placeholder
        '''
        return 1
