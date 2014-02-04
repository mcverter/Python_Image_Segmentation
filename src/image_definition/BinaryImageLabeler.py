'''
Finds the different regions within an image
'''
import numpy as np


BACKGROUND = 1

class EquivalenceEntry(object):
    '''
    Container for labels that seem to be equivalent

    Attributes
    ----------
    elements : Array
       Array of equivalent labels
    '''
    def __init__(self):
        '''
        Initialize empty array
        '''
        self.elements = []

    def add(self, value):
        '''
        Adds label to equivalence set

        Parameters
        ----------
        value : int
            Label added to equivalency array

        '''
        self.elements.append(value)

class EquivalenceTable(object):
    '''
    Collection of equivalency entries

    Attributes
    ----------
    entries : Array 
        Collection of EquivalenceEntry
        
    '''
    def __init__(self):
        '''
        Initializes entries to empty
        '''
        self.entries = []

    def add_equivalence_label(self, value_1, value_2):
        '''
        Merges together two equivalency label sets

        Parameters
        ----------
        value_1, value_2 : int
             Equivalent labels for graph regions
        '''
        if (value_1 == value_2 or value_1 < 0 or value_2 < 0):
            return
        equivalency_a = self.get_equivalence_label(value_1)
        equivalency_b = self.get_equivalence_label(value_2)
        if (equivalency_a != equivalency_b):
            for entry in self.entries[equivalency_a]:
                self.entries[equivalency_b].append(entry)
        self.entries[equivalency_a] = None


    def get_equivalence_label (self, aaa):
        '''
        Returns the representative value for the set containing aaa

        Parameters
        ----------
        aaa : int
           Label found on graph

        Returns
        -------
        int
           The representative label of the equivalency set

        '''
        for entry in (self.entries):
            for value in (entry.entries):
                if value == aaa:
                    return value
        return aaa
           

class BinaryImageLabeler(object):
    '''
    Labels the connected regions of an image 
    '''
    def __init__(self):
        '''
        Initializes equivalence table
        '''
        self.equivalency_table = EquivalenceTable()

    def label_binary_image(self, image):
        '''
        Labels the connected regions of an image 

        Parameters
        ----------
        image : nparray
             An array consisting of independant pixels

        Returns
        -------
        nparray
            An array with connected pixels given the same label
        '''
        dimensions = image.shape()
        value_1 = 0
        value_2 = 0
        value_3 = 0
        value_4 = 0
        label_b = 0
        label_c = 0
        label_d = 0
        labeled_image = np.zeros(dimensions)
        colors = []
        i_label_colors = 0

        for yyy in range (dimensions[0]):
            for xxx in range (dimensions[1]):
                value_1 = image[yyy][xxx]
                if (yyy-1 >=0):
                    label_b = labeled_image[yyy-1][xxx]
                    value_b = [yyy-1][xxx]
                if (xxx-1 >=0):
                    label_c = labeled_image[yyy][xxx-1]
                    value_c = [yyy][xxx-1]
                if (xxx-1 >=0 and yyy-1 >=0):
                    label_d = labeled_image[yyy-1][xxx-1]
                    value_d = [yyy-1][xxx-1]
                if (value_1 == 0):
                    labeled_image[yyy][xxx] = BACKGROUND
                else:
                    if (label_d > 0):
                        labeled_image[yyy][xxx] = label_d
                    else:
                        if (label_c > 0):
                            if (label_b>0):
                                if (label_b == label_c):
                                    labeled_image[yyy][xxx] = label_b
                                else :
                        
                                    labeled_image[yyy][xxx] = label_b
                                    self.equivalency_table.add_equivalence_label(label_b, label_c)
                        else:
                            if (label_b>0):
                                labeled_image[yyy][xxx] = label_b
                            else:
                                labeled_image[yyy][xxx] = i_label_colors
                                i_label_colors += 1
        # second pass
        label = 0
        if ( self.equivalency_table.len() == 0):
            for yyy in range (dimensions[0]):
                for xxx in range (dimensions[1]):
                    if (labeled_image[yyy][xxx]>0):
                        labeled_image[yyy][xxx] = i_label_colors
            return
        for yyy in range (dimensions[0]):
            for xxx in range (dimensions[1]):
                color_index = 0
                label = labeled_image[yyy][xxx]
                if (label != 0):
                    equivalence_value = self.equivalency_table.get_equivalence_label(label)
                    for color in range (i_label_colors):
                        if (color==color_index):
                            colors[color_index] = equivalence_value
                        labeled_image[yyy][xxx] = color+1
        return labeled_image
