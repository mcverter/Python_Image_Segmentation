import pdb

class Arc(object):
    '''
    Connections between nodes

    head : Node
      Node the arc points to 
    next : Arc
      Next arc with the same originating node
    reverse_arc : Arc
      Reverse arc
    residual_capcity : int
      Residual capacity




	/* arc structure */
	typedef struct arc_st
	{
		node_st			*head;		/* node the arc points to */
		arc_st			*next;		/* next arc with the same originating node */
		arc_st			*sister;	/* reverse arc */

		captype			r_cap;		/* residual capacity */
	} arc;

    '''


    def __init__(self, name):
        '''
        Initializes all member variables
        '''
        self.name = name
        self.head = None 
        self.next_arc = None
        self.reverse_arc = None
        self.arc_capacity = 0


    def __looper__ (self):
        self.reverse_arc = self
        self.next_arc = self
    

# TERMINALS
SOURCE = 0
SINK = 1


class NodePtr(object):
    '''
    	/* 'pointer to node' structure */
	typedef struct nodeptr_st
	{
		node_st			*ptr;
		nodeptr_st		*next;
	} nodeptr;


    '''
    def __init__(self):
        self.ptr = None;
        self.next = None; 



class Node(object):
    '''
    Graph Node

    Attributes
    ----------
    first : Arc
       First outcoming arc
    parent : Arc
       Parent of node
    next : Node
       Next active node
       or to itself if it is the last node in the list
    timestamp : int
       Time when distance was computed
    distance : int
       Distance to the terminal
    is_sink_or_source : short	
        Flag for belonging to source or sink tree
    residual_capacity : int
        Residual capcity of node to sink or source
        if tr_cap > 0 then tr_cap is residual capacity 
        of the arc SOURCE->node
        otherwise -tr_cap is residual capacity 
        of the arc node->SINK 


	/* node structure */
	typedef struct node_st
	{
		arc_st			*first;		/* first outcoming arc */

		arc_st			*parent;	/* node's parent */
		node_st			*next;		/* pointer to the next active node
									   (or to itself if it is the last node in the list) */
		int				TS;			/* timestamp showing when DIST was computed */
		int				DIST;		/* distance to the terminal */
		short			is_sink;	/* flag showing whether the node is in the source or in the sink tree */

		captype			tr_cap;		/* if tr_cap > 0 then tr_cap is residual capacity of the arc SOURCE->node
									   otherwise         -tr_cap is residual capacity of the arc node->SINK */
	} node;


    '''
    def __init__(self, name):        
        '''
        Initializes member variables
        '''
        self.name = name
        self.first = None
        self.parent = None
        self.next = None
        self.timestamp = 0
        self.distance = 0
        self.source_or_sink = 0
        self.node_capacity = 0
    
    def is_sink(self):
        '''
        Whether node is part of sink tree
        
        Returns
        -------
        boolean
           Whether node is part of sink tree
        '''
        return self.source_or_sink == SINK

    def set_sink(self):
        '''
        Marks node as part of sink tree
        '''
        self.source_or_sink = SINK

    def set_source(self):
        '''
        Marks node as part of source tree
        '''
        self.source_or_sink = SOURCE


    def is_source(self):
        '''
        Whether node is part of source tree
        
        Returns
        -------
        boolean
           Whether node is part of source tree
        '''
        return self.source_or_sink == SOURCE





'''

'''





class BoykovKolmogorovGraph (object):
    '''
    Python adaptation of the Graph Cut Algorithm by Boykov and Kolmogorov



Graph::Graph(void (*err_function)(char *))
{
	error_function = err_function;
	node_block = new Block<node>(NODE_BLOCK_SIZE, error_function);
	arc_block  = new Block<arc>(NODE_BLOCK_SIZE, error_function);
	flow = 0;
}


/*
	special constants for node->parent
*/
#define TERMINAL ( (arc *) 1 )		/* to terminal */
#define ORPHAN   ( (arc *) 2 )		/* orphan */

#define INFINITE_D 1000000000		/* infinite distance to the terminal */


class Graph
{
public:
	typedef enum
	{
		SOURCE	= 0,
		SINK	= 1
	} termtype; /* terminals */

	/* Type of edge weights.
	   Can be changed to char, int, float, double, ... */
	typedef float captype;
	/* Type of total flow */
	typedef int flowtype;

	typedef void * node_id;

	/* interface functions */

	/* Constructor. Optional argument is the pointer to the
	   function which will be called if an error occurs;
	   an error message is passed to this function. If this
	   argument is omitted, exit(1) will be called. */



	Graph(void (*err_function)(char *) = NULL);

	/* Destructor */
	~Graph();

	/* Adds a node to the graph */
	node_id add_node();

	/* Adds a bidirectional edge between 'from' and 'to'
	   with the weights 'cap' and 'rev_cap' */
	void add_edge(node_id from, node_id to, captype cap, captype rev_cap);

	/* Sets the weights of the edges 'SOURCE->i' and 'i->SINK'
	   Can be called at most once for each node before any call to 'add_tweights'.
	   Weights can be negative */
	void set_tweights(node_id i, captype cap_source, captype cap_sink);

	/* Adds new edges 'SOURCE->i' and 'i->SINK' with corresponding weights
	   Can be called multiple times for each node.
	   Weights can be negative */

	void add_tweights(node_id i, captype cap_source, captype cap_sink);

	/* After the maxflow is computed, this function returns to which
	   segment the node 'i' belongs (Graph::SOURCE or Graph::SINK) */
	termtype what_segment(node_id i);

	/* Computes the maxflow. Can be called only once. */
	flowtype maxflow();




	/* functions for processing active list */
	void set_active(node *i);
	node *next_active();

	void maxflow_init();
	void augment(arc *middle_arc);
	void process_source_orphan(node *i);
	void process_sink_orphan(node *i);
};




	node				*queue_first[2], *queue_last[2];	/* list of active nodes */
	nodeptr				*orphan_first, *orphan_last;		/* list of pointers to orphans */
	int					TIME;								/* monotonically increasing global counter */



	flowtype			flow;		/* total flow */
	struct arc_st;

    '''

    def __init__(self):

        '''
        Initializes the values of the Graph 
        
        /* list of active nodes */
	node				*queue_first[2], 
        node        *queue_last[2];	
	nodeptr				*orphan_first, 
        /* list of pointers to orphans */
        nodeptr                       *orphan_last;	
        /* monotonically increasing global counter */	
	int					TIME;	
	
        /* total flow */
        flowtype			flow;		
	struct arc_st;

        '''
        self.flow = 0
        self.nodes = []
        self.arcs = []
        self.active_nodes = []
        self.orphan_nodes = []
        self.orphan = None
        self.terminal = None
        self.orphan_first = None
        self.orphan_last = None
        self.queue_first = None
        self.queue_last = None
        self.time = 0
        self.flow = 0 

    def add_node(self, name):
        '''
	Adds a node to the graph 
        
        Parameters
        ----------
        value : Node
            Value added to the graph

Graph::node_id Graph::add_node()
{
	node *i = node_block -> New();

	i -> first = NULL;
	i -> tr_cap = 0;

	return (node_id) i;
}

        '''
        n = Node(name)
        self.nodes.append(n)
        return n;


    def add_edge(self, name, from_node, to_node, forward_capacity, reverse_capacity):
        '''
        Adds bidirectional edge to the graph

        Parameters
        ----------
        from_node, to_node : Node
             Connected vertexes
        forward_capacity, reverse_capacity : float
             Weight of edges between nodes


	/* Adds a bidirectional edge between 'from' and 'to'
	   with the weights 'cap' and 'rev_cap' */

void Graph::add_edge(node_id from, node_id to, captype cap, captype rev_cap)
{
	arc *a, *a_rev;

	a = arc_block -> New(2);
	a_rev = a + 1;

	a -> sister = a_rev;
	a_rev -> sister = a;
	a -> next = ((node*)from) -> first;
	((node*)from) -> first = a;
	a_rev -> next = ((node*)to) -> first;
	((node*)to) -> first = a_rev;
	a -> head = (node*)to;
	a_rev -> head = (node*)from;
	a -> r_cap = cap;
	a_rev -> r_cap = rev_cap;
}

        '''

#    def add_edge(self, name, from_node, to_node, forward_capacity, reverse_capacity):

        print "Add Edge " + " " + name + " " + from_node.name + " " + to_node.name + " " + str(forward_capacity) + " " + str(reverse_capacity)
#        pdb.set_trace()
        arc = Arc(name)
        reverse_arc = Arc("reverse_" + name)

        arc.reverse_arc = reverse_arc
        reverse_arc.reverse_arc = arc

        arc.next = from_node.first
        from_node.first = arc

        reverse_arc.next = to_node.first
        to_node.first = reverse_arc

        arc.head = to_node
        reverse_arc.head = from_node

        arc.arc_capacity = forward_capacity
        reverse_arc.arc_capacity = reverse_capacity

        



    def set_tweights(self, node_id, source_capacity, sink_capacity):
        '''
        Sets weights of nodes to source and sink

        Parameters
        ----------
        node_id, to_node : Node
             Graph vertex
        source_capacity : float
             Weight of edge to source
        sink_capacity :  float
             Weight of edge to sink

	/* Sets the weights of the edges 'SOURCE->i' and 'i->SINK'
	   Can be called at most once for each node before any call to 'add_tweights'.
	   Weights can be negative */

void Graph::set_tweights(node_id i, captype cap_source, captype cap_sink)
{
	flow += (cap_source < cap_sink) ? cap_source : cap_sink;
	((node*)i) -> tr_cap = cap_source - cap_sink;
}


        '''
        if (source_capacity < sink_capacity):
            self.flow += source_capacity
        else:
            self.flow += sink_capacity
        node_id.node_capacity = source_capacity - sink_capacity


    def add_tweights(self, node_id, source_capacity, sink_capacity):
        '''
	Adds new weighted edges to source and sink

        Parameters
        ----------
        node_id, to_node : Node
             Graph vertex
        source_capacity : float
             Weight of edge to source
        sink_capacity :  float
             Weight of edge to sink


	/* Adds new edges 'SOURCE->i' and 'i->SINK' with corresponding weights
	   Can be called multiple times for each node.
	   Weights can be negative */

void Graph::add_tweights(node_id i, captype cap_source, captype cap_sink)
{
	register captype delta = ((node*)i) -> tr_cap;
	if (delta > 0) cap_source += delta;
	else           cap_sink   -= delta;
	flow += (cap_source < cap_sink) ? cap_source : cap_sink;
	((node*)i) -> tr_cap = cap_source - cap_sink;
}


        '''


        delta  = node_id.node_capacity
        if (delta > 0):
            source_capacity += delta
        else:
            sink_capacity -= delta
        if (source_capacity < sink_capacity):
            self.flow += source_capacity
        else:
            self.flow += sink_capacity
        node_id.node_capacity = source_capacity - sink_capacity



