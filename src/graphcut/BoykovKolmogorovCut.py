from BoykovKolmogorovGraph import BoykovKolmogorovGraph , Node, Arc , NodePtr, SINK, SOURCE
import pdb

INFINITE_D = 1000000000
#pdb.set_trace()		
TERMINAL = Arc("TERMINAL")
TERMINAL.__looper__()

ORPHAN =  Arc("ORPHAN")
ORPHAN.__looper__()

class BoykovKolmogorovCut(object):
    
    def __init__(self, graph):
        '''

/***********************************************************************/

	node				*queue_first[2], *queue_last[2];	/* list of active nodes */
	nodeptr				*orphan_first, *orphan_last;		/* list of pointers to orphans */
	int					TIME;								/* monotonically increasing global counter */

/***********************************************************************/

	/* functions for processing active list */
	void set_active(node *i);
	node *next_active();

	void maxflow_init();
	void augment(arc *middle_arc);
	void process_source_orphan(node *i);
	void process_sink_orphan(node *i);
};
        '''
        self.graph = graph
        self.queue_first = [None, None]
        self.queue_last = [None, None]
        self.orphan_first = []
        self.orphan_last = []
	self.TIME = 0;					  
        self.flow = 0



    def maxflow(self):
        '''


3.2 Details of Implementation 

Assume that we have a directed graph G = (V,E). As for any augmenting path algorithm, we will maintain a flow f and the residual graph Gf (see Section 2.2). We will keep the lists of all active nodes, A, and all orphans, O. 


The general structure of the algorithm is: 

initialize: S = {s},T = {t},A = {s,t},O =  0

while true 
    grow S or T to find an augmenting path P from s to t 
    if P = 0 terminate 
    augment on P 
    adopt orphans 

end while 

The details of the growth, augmentation, and adoption stages are described below. It is convenient to store content of search trees S and T via flags TREE(p) indicating afilliation of each node p so that . 



. 

TREE(p)= T if p in T 
       . S if p in S
         0 if p is free 

 If node p belongs to one of the search trees then the information about its parent will be stored as PARENT(p). Roots of the search trees(the source and the sink), orphans, and all free nodes have no parents, t.e. PARENT(p)= . We will also use notation tree cap(p. q)to describe residual capacity of either edge(p,q) if TREE(p)= S or edge(q,p)if TREE(p)= T. These edges should be non-saturated in order for node p to be a valid parent of its child q depending on the search tree. 




GROWTH STAGE
------------
At the growth stage the search trees expand. The active nodes explore adjacent non-saturated edges and acquire new children from a set of free nodes. The newly acquired nodes become active members of the corresponding search trees. As soon as all neighbors of a given active node are explored the active node becomes passive. The growth stage terminates if an active node encounters a neighboring node that belongs to the opposite tree. In this case we detect a path from the source to the sink, as shown in Figure 4. 

3.2.1 Growth stage: 

At this stage active nodes acquire new children from a set of free nodes. 

while A  != 0 
      pick an active node p IN A 
      for every neighbor q such that tree.cap(p -> q)> 0 
         if TREE(q) = 0 
         then 
              add q to search tree as an active node: 
              TREE(q):= TREE(p), 
              PARENT(q):= p, 
              A = A UNION {q} 
          if TREE(q) != 0  && TREE(q)!= TREE(p) 
          then 
              return P = PATH(s->t) 
     end for 
     remove p from A 
end while 
return P = 0



AUGMENTATION STAGE
------------------

The augmentation stage augments the path found at the growth stage. Since we push through the largest flow possible some edge(s) in the path become saturated. Thus,some of the nodes in the trees S and T may become orphans, that is, the edges linking them to their parents are no longer valid(they are saturated). In fact,the augmentation phase may split the search trees S and T into forests. The source s and the sink t are still roots of two of the trees while orphans form roots of all other trees. 


3.2.2 Augmentation stage: 

The input for this stage is a path P from s to t. Note that the orphan set is empty in the beginning of the stage, but there might be some orphans in the end since at least one edge in P becomes saturated. 

find the bottleneck capacity DELTA on P 
update the residual graph by pushing flow DELTA through P 
for each edge (p,q) in P that becomes saturated 
    if TREE(p)= TREE(q)= S 
    then 
         set PARENT(q):= 0 
         set O := O UNION {q} 
    if TREE(p)= TREE(q)= T 
    then 
         set PARENT(p):= 0
         set O := O UNION {p} 
end for 




ADOPTION STAGE
--------------

The goal of the adoption stage is to restore single-tree structure of sets S and T with roots in the source and the sink. At this stage we try to find a new valid parent for each orphan. A new parent should belong to the same set, S or T, as the orphan. A parent should also be connected through a non-saturated edge. If there is no qualifying parent we remove the orphan from S or T and make it a free node. We also declare all its former children as orphans. The stage terminates when no orphans are left and, thus, the search tree structures of S and T are restored. Since some orphan nodes in S and T may become free the adoption stage results in contraction of these sets. 




3.2.3 Adoption stage: 

During this stage all orphan nodes in O are processed until O becomes empty. Each node p being processed tries to find a new valid parent within the same search tree; in case of success p remains in the tree but with a new parent, otherwise it becomes a free node and all its children are added to O. 

while O != 0
    pick an orphan node p IN O and remove it from O 
    process p 
end while 


The operation "process p" consists of the following steps. 
(1) First we are trying to find a new valid parent for p among its neighbors. A valid parent q should satisfy: TREE(q)= TREE(p), tree_cap(q -> p)> 0, and the "origin" of q should be either source or sink. Note that the last condition is necessary because during adoption stage some of the nodes in the search trees S or T may originate from orphans.

 
If node p finds a new valid parent q then we set PARENT(p)= q. In this case p remains inits search tree and the active(or passive) status of p remains unchanged. If p does not find a valid parent then p becomes a free node and the following operations are performed: 

 scan all neighbors q of p such that TREE(q)= TREE(p): 
     if tree_cap(q->p)>0 
     then
          add q to the active set A
     if PARENT(q)= p 
     then
          add q to the set of orphans O 
          set PARENT(q):=  0

 TREE(p):= 0 
 A := A-{p} 

Note that as p becomes free all its neighbors connected through non-saturated edges should became active. It may happen that some neighbor q did not qualify as a valid parent during adoption stage because it did not originate from the source or the sink. However, this node could be a valid parent after adoption stage is finished. At this point q must have active status as it is located next to a free node p. 





ITERATION
---------

After the adoption stage is completed the algorithm returns to the growth stage. The algorithm terminates when the search trees S and T can not grow(no active nodes) and the trees are separated by saturated edges. This implies that a maximum flow is achieved. The corresponding minimum cut can be determined by S = S and T = T. 



        Executes the Max Flow/Min Cut 


	/* Computes the maxflow. Can be called only once. */

Graph::flowtype Graph::maxflow()
{
	node *i, *j, *current_node = NULL;
	arc *a;
	nodeptr *np, *np_next;

	maxflow_init();
	nodeptr_block = new DBlock<nodeptr>(NODEPTR_BLOCK_SIZE, error_function);

	while ( 1 )
	{
		if (i=current_node)
		{
			i -> next = NULL; /* remove active flag */
			if (!i->parent) i = NULL;
		}
		if (!i)
		{
			if (!(i = next_active())) break;
		}

		/* growth */
		if (!i->is_sink)
		{
			/* grow source tree */
			for (a=i->first; a; a=a->next)
			if (a->r_cap)
			{
				j = a -> head;
				if (!j->parent)
				{
					j -> is_sink = 0;
					j -> parent = a -> sister;
					j -> TS = i -> TS;
					j -> DIST = i -> DIST + 1;
					set_active(j);
				}
				else if (j->is_sink) break;
				else if (j->TS <= i->TS &&
				         j->DIST > i->DIST)
				{
					/* heuristic - trying to make the distance from j to the source shorter */
					j -> parent = a -> sister;
					j -> TS = i -> TS;
					j -> DIST = i -> DIST + 1;
				}
			}
		}
		else
		{
		
			for (a=i->first; a; a=a->next)
			if (a->sister->r_cap)
			{
				j = a -> head;
				if (!j->parent)
				{
					j -> is_sink = 1;
					j -> parent = a -> sister;
					j -> TS = i -> TS;
					j -> DIST = i -> DIST + 1;
					set_active(j);
				}
				else if (!j->is_sink) { a = a -> sister; break; }
				else if (j->TS <= i->TS &&
				         j->DIST > i->DIST)
				{
					/* heuristic - trying to make the distance from j to the sink shorter */
					j -> parent = a -> sister;
					j -> TS = i -> TS;
					j -> DIST = i -> DIST + 1;
				}
			}
		}

		TIME ++;

		if (a)
		{
			i -> next = i; /* set active flag */
			current_node = i;

			/* augmentation */
			augment(a);
			/* augmentation end */

			/* adoption */
			while (np=orphan_first)
			{
				np_next = np -> next;
				np -> next = NULL;

				while (np=orphan_first)
				{
					orphan_first = np -> next;
					i = np -> ptr;
					nodeptr_block -> Delete(np);
					if (!orphan_first) orphan_last = NULL;
					if (i->is_sink) process_sink_orphan(i);
					else            process_source_orphan(i);
				}

				orphan_first = np_next;
			}
			/* adoption end */
		}
		else current_node = NULL;
	}

	delete nodeptr_block;

	return flow;
}



        '''


        
        nnn = Node("foo")
        jjj = Node("foo")
        current_node = None
        aaa = Arc("foo")
        np = NodePtr()
        np_next = NodePtr()
             
     
        self.maxflow_init()
        
        #arc_list = []


        while (True):
            nnn = current_node

            if (nnn != None):
                #  /* remove active flag */
                nnn.next = None 
                if (nnn.parent == None):
                    nnn = None
            if (nnn == None):
                nnn = self.next_active()
                if (nnn == None):
                    break

            print "In maxflow WHILE "
            #/* growth */
            if (nnn.is_sink()==False):
                print "growing SOURCE tree starting with node " +  nnn.name
##                pdb.set_trace()
                aaa = nnn.first
                while (aaa != None):
                    print "checking the arc " + aaa.name
                    if (aaa.arc_capacity != 0):
                        jjj = aaa.head
                        print "now looking at the connecting node " + jjj.name
                        if (jjj.parent == None):
                            jjj.set_source()
                            jjj.parent = aaa.reverse_arc
                            jjj.timestamp = nnn.timestamp
                            jjj.distance = nnn.distance+1
                            self.set_active(jjj)
                        elif (jjj.is_sink()):
                            break
                        elif(jjj.timestamp <= nnn.timestamp 
                             and jjj.distance > nnn.distance):
                            #	heuristic - trying to make the distance from j to the source shorter */
                            jjj.parent = aaa.reverse_arc
                            jjj.timestamp = nnn.timestamp
                            jjj.distance = nnn.distance + 1
                    aaa = aaa.next_arc
            else:
                print "growing SINK tree starting with node " +  nnn.name
            # /* grow sink tree */
                aaa = nnn.first
                while (aaa != None):
                    print "checking the arc " + aaa.name
                    if (aaa.reverse_arc.arc_capacity != 0):
                        jjj = aaa.head
                        print "now looking at the connecting node " + jjj.name
                        if (jjj.parent == None):
                            jjj.set_sink()
                            jjj.parent = aaa.reverse_arc
                            jjj.timestamp = nnn.timestamp
                            jjj.distance = nnn.distance+1
                            self.set_active(jjj)
                        elif (jjj.is_sink()):
                            aaa = aaa.reverse_arc
                            break
                        elif(jjj.timestamp <= nnn.timestamp 
                             and jjj.distance > nnn.distance):
                            #	heuristic - trying to make the distance from j to the sink shorter */
                            jjj.parent = aaa.reverse_arc
                            jjj.timestamp = nnn.timestamp
                            jjj.distance = nnn.distance + 1
                    aaa = aaa.next_arc
            self.TIME += 1                
            if (aaa):
                #  /* set active flag */
                nnn.next = nnn  
                self.current_node = nnn
                #   /* augmentation */
                self.augment (aaa)
                #   /* augmentation end */
    

                #   /* adoption */
                np = self.orphan_first
                print "Now in adoption"
                while (np != None):
                    #pdb.set_trace()
                    print np
                    np_next = np.next
                    np.next = None
                    while (np != None):
                        self.orphan_first = np.next
                        nnn = np.ptr
                        np = None
                        print "Next adoptable node is " + nnn.name
                        if (self.orphan_first == None):
                            self.orphan_last = None
                        if (nnn.is_sink() == True):
                            self.process_sink_orphan(nnn)
                        else:
                            self.process_source_orphan(nnn)
                            current = None
                    orphan_first = np_next
                # 	/* adoption end */
            else:
                current_node = None
        return self.flow

    '''
    /*
    Functions for processing active list.
    i->next points to the next node in the list
    (or to i, if i is the last node in the list).
    If i->next is NULL iff i is not in the list.
    
	There are two queues. Active nodes are added
	to the end of the second queue and read from
	the front of the first queue. If the first queue
	is empty, it is replaced by the second queue
	(and the second queue becomes empty).
        */
        '''


    def set_active(self, nnn):
        '''
        Processes the Active Node List

        Function for processing active list.
	nnn.next points to the next node 
        in the list (or to nnn, if nnn is the 
        last node in the list).
	
        If nnn.next is NULL iff nnn is not 
        in the list.

	There are two queues. 
        Active nodes are added
	to the end of the second queue 
        and read from
	the front of the first queue. 
        If the first queue is empty, 
        it is replaced by the second queue
	(and the second queue becomes empty).

        Parameters 
        ----------
        nnn : Node
            Next enqueued node
 
/*
	Returns the next active node.
	If it is connected to the sink, it stays in the list,
	otherwise it is removed from the list
*/


inline void Graph::set_active(node *i)
{
	if (!i->next)
	{
		/* it's not in the list yet */
		if (queue_last[1]) queue_last[1] -> next = i;
		else               queue_first[1]        = i;
		queue_last[1] = i;
		i -> next = i;
	}
}



       '''

        if (nnn.next == None):
            # 		/* it's not in the list yet */
            if (self.queue_last[1] != None):
                self.queue_last[1].next = nnn
            else :
                self.queue_first[1] = nnn
            self.queue_last[1] = nnn
            nnn.next = nnn

    def next_active(self):
        '''
        Gets the next active node
       
	Returns the next active node.
	If it is connected to the sink, 
        it stays in the list,
	otherwise it is removed from the list

        Returns
        -------
        Node
            Next active node


inline Graph::node * Graph::next_active()
{
	node *i;

	while ( 1 )
	{
		if (!(i=queue_first[0]))
		{
			queue_first[0] = i = queue_first[1];
			queue_last[0]  = queue_last[1];
			queue_first[1] = NULL;
			queue_last[1]  = NULL;
			if (!i) return NULL;
		}

		/* remove it from the active list */
		if (i->next == i) queue_first[0] = queue_last[0] = NULL;
		else              queue_first[0] = i -> next;
		i -> next = NULL;

		/* a node in the list is active iff it has a parent */
		if (i->parent) return i;
	}
}

        '''
        nnn = Node("foo")
        while (True):
            nnn = self.queue_first[0]
            if (self.queue_first[0] == None):
                nnn = self.queue_first[1]
                self.queue_first[0] = nnn 
                self.queue_last[0] = self.queue_last[1]
                self.queue_first[1] = None
                self.queue_last[1] = None
                if (nnn == None):
                    return None
            #	/* remove it from the active list */
            if (nnn.next == nnn):
                self.queue_first[0] = None
                self.queue_last [0] = None
            else :
                self.queue_first [0] = nnn.next
            nnn.next = None
            # /* a node in the list is active iff it has a parent */
            if (nnn.parent != None):
                return nnn


    def maxflow_init(self):
        '''
        Initializes the Max Flow / Min Cut



void Graph::maxflow_init()
{
	node *i;

	queue_first[0] = queue_last[0] = NULL;
	queue_first[1] = queue_last[1] = NULL;
	orphan_first = NULL;

	for (i=node_block->ScanFirst(); i; i=node_block->ScanNext())
	{
		i -> next = NULL;
		i -> TS = 0;
		if (i->tr_cap > 0)
		{
			/* i is connected to the source */
			i -> is_sink = 0;
			i -> parent = TERMINAL;
			set_active(i);
			i -> TS = 0;
			i -> DIST = 1;
		}
		else if (i->tr_cap < 0)
		{
			/* i is connected to the sink */
			i -> is_sink = 1;
			i -> parent = TERMINAL;
			set_active(i);
			i -> TS = 0;
			i -> DIST = 1;
		}
		else
		{
			i -> parent = NULL;
		}
	}
	TIME = 0;
}


        '''
        for nnn in (self.graph.nodes):
            nnn.next = None
            nnn.timestamp = 0
            if (nnn.node_capacity > 0):
                print "NODE " + nnn.name + ":  initalized to source" 
                nnn.set_source()
                nnn.parent = TERMINAL
                self.set_active(nnn)
                nnn.timestamp = 0
                nnn.distance = 1
            elif (nnn.node_capacity < 0):
                print "NODE " + nnn.name + ":  initalized to sink" 
                nnn.set_sink()
                nnn.parent = TERMINAL
                self.set_active(nnn)
                nnn.timestamp = 0
                nnn.distance = 1
            else :
                print "NODE " + nnn.name + ":  not initialized"
                nnn.parent = None
            
        self.TIME = 0



    def augment(self, middle_arc):
        '''
        Adjusts the edge weights to find Max Flow

        Proceeds as follows
        (1) Finds bottleneck capacity 
           (a) In the source tree 
	   (b) Inthe sink tree 
	(2)  Augments Edges 
	   (a) In the source tree 
               (i) adds orphaned nodes
                   to the adoption list 
	   (a) In the sink tree 
               (i) adds orphaned nodes
                   to the adoption list 

void Graph::augment(arc *middle_arc)
{
	node *i;
	arc *a;
	captype bottleneck;
	nodeptr *np;


	/* 1. Finding bottleneck capacity */
	/* 1a - the source tree */
	bottleneck = middle_arc -> r_cap;
	for (i=middle_arc->sister->head; ; i=a->head)
	{
		a = i -> parent;
		if (a == TERMINAL) break;
		if (bottleneck > a->sister->r_cap) bottleneck = a -> sister -> r_cap;
	}
	if (bottleneck > i->tr_cap) bottleneck = i -> tr_cap;
	/* 1b - the sink tree */
	for (i=middle_arc->head; ; i=a->head)
	{
		a = i -> parent;
		if (a == TERMINAL) break;
		if (bottleneck > a->r_cap) bottleneck = a -> r_cap;
	}
	if (bottleneck > - i->tr_cap) bottleneck = - i -> tr_cap;


	/* 2. Augmenting */
	/* 2a - the source tree */
	middle_arc -> sister -> r_cap += bottleneck;
	middle_arc -> r_cap -= bottleneck;
	for (i=middle_arc->sister->head; ; i=a->head)
	{
		a = i -> parent;
		if (a == TERMINAL) break;
		a -> r_cap += bottleneck;
		a -> sister -> r_cap -= bottleneck;
		if (!a->sister->r_cap)
		{
			/* add i to the adoption list */
			i -> parent = ORPHAN;
			np = nodeptr_block -> New();
			np -> ptr = i;
			np -> next = orphan_first;
			orphan_first = np;
		}
	}
	i -> tr_cap -= bottleneck;
	if (!i->tr_cap)
	{
		/* add i to the adoption list */
		i -> parent = ORPHAN;
		np = nodeptr_block -> New();
		np -> ptr = i;
		np -> next = orphan_first;
		orphan_first = np;
	}
	/* 2b - the sink tree */
	for (i=middle_arc->head; ; i=a->head)
	{
		a = i -> parent;
		if (a == TERMINAL) break;
		a -> sister -> r_cap += bottleneck;
		a -> r_cap -= bottleneck;
		if (!a->r_cap)
		{
			/* add i to the adoption list */
			i -> parent = ORPHAN;
			np = nodeptr_block -> New();
			np -> ptr = i;
			np -> next = orphan_first;
			orphan_first = np;
		}
	}
	i -> tr_cap += bottleneck;
	if (!i->tr_cap)
	{
		/* add i to the adoption list */
		i -> parent = ORPHAN;
		np = nodeptr_block -> New();
		np -> ptr = i;
		np -> next = orphan_first;
		orphan_first = np;
	}


	flow += bottleneck;
}



        '''
#        pdb.set_trace()
        nnn = Node
        aaa = Arc("foo")
        nptr = NodePtr()
        bottleneck = 0
        
        # /* 1. Finding bottleneck capacity */
	# /* 1a - the source tree */
        bottleneck = middle_arc.arc_capacity
        nnn = middle_arc.reverse_arc.head
        while (1):
            aaa = nnn.parent
            if (aaa==TERMINAL):
                break
            if (bottleneck > (aaa.reverse_arc.arc_capacity)):
                bottleneck =  aaa.reverse_arc.arc_capacity
            nnn=aaa.head

        if (bottleneck > nnn.node_capacity):
            bottleneck = nnn.node_capacity
            
        # 	/* 1b - the sink tree */
        nnn = middle_arc.head
        while (1):
            aaa = nnn.parent
            if (aaa==TERMINAL):
                break
            if (bottleneck > aaa.arc_capacity):
                bottleneck = aaa.arc_capacity
            
        if (bottleneck > -1*(nnn.node_capacity)):
            bottleneck = -1*(nnn.node_capacity)

	#/* 2. Augmenting */
	#/* 2a - the source tree */
        middle_arc.reverse_arc.arc_capacity += bottleneck
        middle_arc.arc_capacity -= bottleneck

        nnn = middle_arc.reverse_arc.head
        while (True):
            aaa = nnn.parent
            if (aaa==TERMINAL):
                break
            aaa.arc_capacity += bottleneck
            aaa.reverse_arc.arc_capacity -= bottleneck
            if (aaa.reverse_arc.arc_capacity == 0):
                # /* add i to the adoption list */
                nnn.parent = ORPHAN
                nptr  = NodePtr()
                nptr.ptr = nnn
                nptr.next = self.orphan_first
                self.orphan_first = nptr
            nnn=aaa.head


        nnn.node_capacity -= bottleneck
        if (nnn.node_capacity == 0):
            # /* add i to the adoption list */
            nnn.parent = ORPHAN
            nptr = NodePtr();
            nptr.ptr = nnn
            nptr.next = self.orphan_first
            self.orphan_first = nptr

        #  /* 2b - the sink tree */
        nnn = middle_arc.head
        while (True):
            aaa = nnn.parent
            if (aaa==TERMINAL):
                break            
            print "Augmenting now.  Arc is " + aaa.name + ".  Node is " + nnn.name
            #pdb.set_trace()
            aaa.reverse_arc.arc_capacity += bottleneck
            aaa.arc_capacity -= bottleneck
            if (aaa.arc_capacity == 0):
                #  /* add i to the adoption list */
                nnn.parent = ORPHAN
                nptr = NodePtr()
                nptr.ptr = nnn
                nptr.next = self.orphan_first
                self.orphan_first = nptr
            nnn = aaa.head


        nnn.node_capacity -= bottleneck
        if (nnn.node_capacity == 0):
            # 	/* add i to the adoption list */
            nnn.parent = ORPHAN
            nptr = NodePtr()
            nptr.ptr = nnn
            nptr.next = self.orphan_first
            self.orphan_first = nptr
        self.flow += bottleneck
        return self.flow
                      
                      

    def process_source_orphan(self, nnn):

        '''
        Tries to find parents nodes orphaned by source augmenation

        Parameters
        ----------
        nnn : Node
            Orphaned node




void Graph::process_source_orphan(node *i)
{
	node *j;
	arc *a0, *a0_min = NULL, *a;
	nodeptr *np;
	int d, d_min = INFINITE_D;

	/* trying to find a new parent */
	for (a0=i->first; a0; a0=a0->next)
	if (a0->sister->r_cap)
	{
		j = a0 -> head;
		if (!j->is_sink && (a=j->parent))
		{
			/* checking the origin of j */
			d = 0;
			while ( 1 )
			{
				if (j->TS == TIME)
				{
					d += j -> DIST;
					break;
				}
				a = j -> parent;
				d ++;
				if (a==TERMINAL)
				{
					j -> TS = TIME;
					j -> DIST = 1;
					break;
				}
				if (a==ORPHAN) { d = INFINITE_D; break; }
				j = a -> head;
			}
			if (d<INFINITE_D) /* j originates from the source - done */
			{
				if (d<d_min)
				{
					a0_min = a0;
					d_min = d;
				}
				/* set marks along the path */
				for (j=a0->head; j->TS!=TIME; j=j->parent->head)
				{
					j -> TS = TIME;
					j -> DIST = d --;
				}
			}
		}
	}

	if (i->parent = a0_min)
	{
		i -> TS = TIME;
		i -> DIST = d_min + 1;
	}
	else
	{
		/* no parent is found */
		i -> TS = 0;

		/* process neighbors */
		for (a0=i->first; a0; a0=a0->next)
		{
			j = a0 -> head;
			if (!j->is_sink && (a=j->parent))
			{
				if (a0->sister->r_cap) set_active(j);
				if (a!=TERMINAL && a!=ORPHAN && a->head==i)
				{
					/* add j to the adoption list */
					j -> parent = ORPHAN;
					np = nodeptr_block -> New();
					np -> ptr = j;
					if (orphan_last) orphan_last -> next = np;
					else             orphan_first        = np;
					orphan_last = np;
					np -> next = NULL;
				}
	o		}
		}
	}
}



        '''
        #pdb.set_trace()

        jjj = Node("foo")
        arc0 = Arc("foo")
        arc0_min = None
        arc = Arc("foo")
        nptr = NodePtr()
        ddd = 0
        d_min = INFINITE_D
        node_list = []
        

	# /* trying to find a new parent */
        arc0 = nnn.first
        while (arc0 != None):
            if (arc0.reverse_arc.arc_capacity != 0):
                jjj = arc0.head
                if (jjj.is_source() and 
                    (jjj.parent != None)):
                    arc = jjj.parent
                    # /* checking the origin of j */
                    ddd = 0
                    while (True):
                        if (jjj.timestamp == self.TIME):
                            ddd += jjj.distance
                            break
                        arc = jjj.parent
                        ddd += 1
                        if (arc==TERMINAL):
                            jjj.timestamp = self.TIME
                            jjj.distance = 1
                            break
                        if (arc==ORPHAN):
                            ddd = INFINITE_D
                            break
                        jjj = arc.head
                    if (ddd < INFINITE_D):
                        # /* j originates from the source - done */
                        if (ddd < d_min):
                            arc0_min = arc0
                            d_min = ddd
                        #  /* set marks along the path */
      
                        jjj = arc0.head

                        while (jjj.timestamp != self.TIME): 
                            jjj.timestamp = self.TIME
                            ddd -= 1
                            jjj.distance = ddd
                            jjj = jjj.parent.head
            arc0=arc0.next_arc


        nnn.parent = arc0_min                               
        if (arc0_min != None):

            nnn.timestamp = self.TIME
            nnn.distance = d_min + 1
        else:
            # /* no parent is found */
            nnn.timestamp = 0

            # 		/* process neighbors */
            arc0 = nnn.first
            while (arc0 != None):
                jjj = arc0.head
                if (jjj.is_source() == True 
                    and jjj.parent != None):
                    arc = jjj.parent
                    if (arc.reverse_arc.arc_capacity != 0):
                        self.set_active(jjj)
                    if (arc != TERMINAL and 
                        arc != ORPHAN and 
                        arc.head == nnn):
			# /* add j to the adoption list */
                        jjj.parent = ORPHAN
                        nptr.ptr = jjj
                        if (self.orphan_last):
                            self.orphan_last.next = nptr
                        else :
                            self.orphan_first = nptr
                        self.orphan_last = nptr
                        nptr.next = None
                arc0 = arc0.next_arc



    def process_sink_orphan(self, nnn):

        '''
        Tries to find parents nodes orphaned by sink augmenation

        Parameters
        ----------
        nnn : Node
            Orphaned node



void Graph::process_sink_orphan(node *i)
{
	node *j;
	arc *a0, *a0_min = NULL, *a;
	nodeptr *np;
	int d, d_min = INFINITE_D;

	/* trying to find a new parent */
	for (a0=i->first; a0; a0=a0->next)
	if (a0->r_cap)
	{
		j = a0 -> head;
		if (j->is_sink && (a=j->parent))
		{
			/* checking the origin of j */
			d = 0;
			while ( 1 )
			{
				if (j->TS == TIME)
				{
					d += j -> DIST;
					break;
				}
				a = j -> parent;
				d ++;
				if (a==TERMINAL)
				{
					j -> TS = TIME;
					j -> DIST = 1;
					break;
				}
				if (a==ORPHAN) { d = INFINITE_D; break; }
				j = a -> head;
			}
			if (d<INFINITE_D) /* j originates from the sink - done */
			{
				if (d<d_min)
				{
					a0_min = a0;
					d_min = d;
				}
				/* set marks along the path */
				for (j=a0->head; j->TS!=TIME; j=j->parent->head)
				{
					j -> TS = TIME;
					j -> DIST = d --;
				}
			}
		}
	}

	if (i->parent = a0_min)
	{
		i -> TS = TIME;
		i -> DIST = d_min + 1;
	}
	else
	{
		/* no parent is found */
		i -> TS = 0;

		/* process neighbors */
		for (a0=i->first; a0; a0=a0->next)
		{
			j = a0 -> head;
			if (j->is_sink && (a=j->parent))
			{
				if (a0->r_cap) set_active(j);
				if (a!=TERMINAL && a!=ORPHAN && a->head==i)
				{
					/* add j to the adoption list */
					j -> parent = ORPHAN;
					np = nodeptr_block -> New();
					np -> ptr = j;
					if (orphan_last) orphan_last -> next = np;
					else             orphan_first        = np;
					orphan_last = np;
					np -> next = NULL;
				}
			}
		}
	}
}

        '''

        jjj = Node("foo")
        arc0 = Arc("foo")
        arc0_min = None
        arc = Arc("foo")
        nptr = NodePtr()
        ddd = 0
        d_min = INFINITE_D
        node_list = []
        

	# /* trying to find a new parent */
        arc0 = nnn.first
        while (arc0 != None):

            print "Now Processing Sink Orphan Node: " + nnn.name + " Arc: " + arc0.name 
            if (arc0.reverse_arc.arc_capacity != 0):
                jjj = arc0.head
                if (jjj.is_sink() == True and 
                    (jjj.parent != None)):
                    arc = jjj.parent
                    # /* checking the origin of j */
                    ddd = 0
                    while (True):
                        if (jjj.timestamp == self.TIME):
                            ddd += jjj.distance
                            break
                        arc = jjj.parent
                        ddd += 1
                        if (arc==TERMINAL):
                            jjj.timestamp = self.TIME
                            jjj.distance = 1
                            break
                        if (arc==ORPHAN):
                            ddd = INFINITE_D
                            break
                        jjj = arc.head
                    if (ddd < INFINITE_D):
                        # /* j originates from the sink - done */
                        if (ddd < d_min):
                            arc0_min = arc0
                            d_min = ddd
                        #  /* set marks along the path */
      
                        jjj = arc0.head

                        while (jjj.timestamp != self.TIME): 
                            jjj.timestamp = self.TIME
                            ddd -= 1
                            jjj.distance = ddd
                            jjj = jjj.parent.head
            arc0=arc0.next_arc


                               
        if (arc0_min != 0):
            nnn.parent = arc0_min
            nnn.timestamp = self.TIME
            nnn.distance = d_min + 1
        else:
            # /* no parent is found */
            nnn.timestamp = 0

            # 		/* process neighbors */
            arc0 = nnn.first
            while (arc0 != None):
                jjj = arc0.head
                if (jjj.is_sink() == True
                    and jjj.parent != None):
                    arc = jjj.parent
                    if (arc.reverse_arc.arc_capacity != 0):
                        self.set_active(jjj)
                    if (arc != TERMINAL and 
                        arc != ORPHAN and 
                        arc.head == nnn):
			# /* add j to the adoption list */
                        jjj.parent = ORPHAN
                        nptr.ptr = jjj
                        if (self.orphan_last):
                            self.orphan_last.next = nptr
                        else :
                            self.orphan_first = nptr
                        self.orphan_last = nptr
                        nptr.next = None
                arc0 = arc0.next_arc




    def what_segment(self, node):
        '''
        Determines whether node belongs to sink or source

        Parameters
        ----------
        node : Node
           Node being evaluated

        Returns
        -------
        short
           Indicates whether node belongs to sink or source

	/* After the maxflow is computed, this function returns to which
	   segment the node 'i' belongs (Graph::SOURCE or Graph::SINK) */
        

Graph::termtype Graph::what_segment(node_id i)
{
	if (((node*)i)->parent && !((node*)i)->is_sink) return SOURCE;
	return SINK;
}

       '''
        if (node.parent == True  and node.is_source()):
            return SOURCE
        return SINK

