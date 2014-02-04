import unittest
import pdb 

from graphcut.BoykovKolmogorovGraph import BoykovKolmogorovGraph, SOURCE, SINK
from graphcut.BoykovKolmogorovCut import BoykovKolmogorovCut


class BoykovKolmogorovTest(unittest.TestCase):

    def set_up(self):

        self.graph = BoykovKolmogorovGraph()

        # Add Nodes
        self.n0 = self.graph.add_node('n0')
        self.n1 = self.graph.add_node('n1') 
        self.n2 = self.graph.add_node('n2') 
        self.n3 = self.graph.add_node('n3') 
        self.n4 = self.graph.add_node('n4') 
        self.n5 = self.graph.add_node('n5') 
        self.n6 = self.graph.add_node('n6') 
        self.n7 = self.graph.add_node('n7') 
        self.n8 = self.graph.add_node('n8') 
        
        # Add Edges
        e_0_1 = self.graph.add_edge('e_0_1', self.n0, self.n1,  4, 4)
        e_1_2 = self.graph.add_edge('e_1_2', self.n1, self.n2, 1, 1)
        e_0_3 = self.graph.add_edge('e_0_3', self.n0, self.n3, 6 ,6)
        e_1_4 = self.graph.add_edge('e_1_4',  self.n1, self.n4, 1, 1)
        e_2_5 = self.graph.add_edge('e_2_5',  self.n2, self.n5 ,6,6 )
        
        e_3_4 = self.graph.add_edge('e_3_4', self.n3, self.n4, 6, 6)
        e_4_5 = self.graph.add_edge('e_4_5',  self.n4, self.n5 ,1, 1)
        e_3_6 = self.graph.add_edge('e_3_6',  self.n3, self.n6, 6 ,6)
        e_4_7 = self.graph.add_edge('e_4_7',  self.n4, self.n7, 1, 1)
        e_5_8 = self.graph.add_edge('e_5_8',  self.n5, self.n8,  6, 6)
        
        
        e_6_7 = self.graph.add_edge('e_6_7',  self.n6, self.n7, 1, 1)
        e_7_8 = self.graph.add_edge('e_7_8',  self.n7, self.n8,  4, 4)
        
        

        self.graph.set_tweights(self.n0,1 ,0 )
        self.graph.set_tweights(self.n1,1, 0)
        self.graph.set_tweights(self.n2,4, 4)
        self.graph.set_tweights(self.n3, 6 , 2)
        self.graph.set_tweights(self.n4,4, 4)
        self.graph.set_tweights(self.n5, 2, 6)
        self.graph.set_tweights(self.n6,4, 4)
        self.graph.set_tweights(self.n7,0, 1)
        self.graph.set_tweights(self.n8,0 ,1)
                
        self.cut = BoykovKolmogorovCut(self.graph)



    def runTest(self):
        # query nodes for segmentation
        self.cut.maxflow()


        print (self.cut.what_segment(self.n0))
        print(self.cut.what_segment(self.n1))
        print(self.cut.what_segment(self.n2))
        print(self.cut.what_segment(self.n3))
        print(self.cut.what_segment(self.n4)) 
        print(self.cut.what_segment(self.n5))
        print(self.cut.what_segment(self.n6))
        print(self.cut.what_segment(self.n7))
        print(self.cut.what_segment(self.n8))


        '''
        self.assertEqual(self.cut.what_segment(self.n0),SOURCE)
        self.assertEqual(self.cut.what_segment(self.n1),SOURCE)
        self.assertEqual(self.cut.what_segment(self.n2),SINK)
        self.assertEqual(self.cut.what_segment(self.n3),SOURCE)
        self.assertEqual(self.cut.what_segment(self.n4),SOURCE) 
        self.assertEqual(self.cut.what_segment(self.n5),SINK)
        self.assertEqual(self.cut.what_segment(self.n6),SOURCE)
        self.assertEqual(self.cut.what_segment(self.n7),SINK)
        self.assertEqual(self.cut.what_segment(self.n8),SINK)
        '''


if __name__ == '__main__':
    test = BoykovKolmogorovTest()
    test.set_up()
    test.runTest()
