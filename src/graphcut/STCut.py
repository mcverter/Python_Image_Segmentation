''' 
This class is the main interface for executing the 
graph cut algorithm given by Boykov and Kolmogorov.

'''


from statistics.frameworks.GraphCutFramework  import GraphCutFramework
from BoykovKolmogorovCut import BoykovKolmogorovGraph
import numpy as np

FLOAT_MIN = -999999
FLOAT_MAX = 999999

class STCut(object):
    ''' 
    This class is the main interface for executing the 
    graph cut algorithm given by Boykov and Kolmogorov.

    Attributes
    ----------

    graph : BoykovKolmogorovGraph
       Python implementation of Graph Cut algorithm
    framework : GraphCutFramework
       Coordinates Image Observations with regional 
       and boundary estimators
    nodes : list
        Array of nodes in the graph
    '''
    
    
    def __init__(self, framework):
        '''
        Initializes member variables
        '''
        self.graph = BoykovKolmogorovGraph()
        self.framework = GraphCutFramework()
        self.nodes = np.zeros(framework.num_nodes())

        
    def execute_cut(self):
        '''
        Creates a segmentation from inputs

        Accepts the graph, nodes,and framework
        and goes through all of the steps of 
        creating a segmentation.

        (1) Initialization 
        (2) Creating Edges
        (3) Finding the MaxFlow/MinCut
        (4) Returning the Paritioned sapace

        Returns
        -------
        nparray 
           Segmentation of the original image
        ''' 
        self.construct_graph_edges()
        self.cut_graph()
        return self.get_result_partition()

    def construct_graph_edges(self):
        '''
        Initializes the graph edges from data in the framework
        '''
        for node in self.nodes:
            neighbor_link_costs = self.framework.get_neighbor_link_cost(node)
            for link in neighbor_link_costs:
                self.graph.add_edge(node, link, 1, 1)  # not sure what WF and WB arw
            st_cost = self.framework.get_st_cost(node)
            self.graph.set_tweights(node, st_cost, 1) # not sure what fWS fWT are
                     
            
            
    def update_st_link(self, node, f_w_s, f_w_t):
        '''
        Gets link costs from framework and adds them to graph
        
        Parameters
        ----------
        node : Node
           Node being updated
        f_w_s :
           Cost to source
        f_w_s :
           Cost to sink
        '''
        st_cost = self.framework.get_st_cost(node)
        self.graph.add_tweights(node, f_w_s, f_w_t)

    def update_graph(self):
        '''
        Updates all link costs
        
        '''
        updated_costs = self.framework.get_all_updated_st_link_costs
        for node in self.nodes:
            self.graph.add_tweights(node, updated_costs.costs, updated_costs.tcost)
        
    def cut_graph(self):
        '''
        Executes Max Flow/Min Cut algorithm
        '''
        self.update_graph()
        self.graph.max_flow()


    def get_result_partition(self):
        '''
        Gets the result of the Graph Cut

        Returns 
        -------
        nparray :
            Partitioned graph
        '''
        result_partition = np.array(self.nodes.size()) 
        for node in self.nodes:
            result_partition = self.graph.what_segment(node)
        return result_partition
        
