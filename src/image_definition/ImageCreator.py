'''
Post Processing after the implementation of the
Graph Cut

Takes the resulting segmentation and converts it to
an image
'''

from ThresholdTracker import ThresholdTracker
from BinaryImageLabeler import BinaryImageLabeler
import numpy as np
import pylab

class ImageCreator(object):
    '''
    Post Processing after the implementation of the
    Graph Cut
    
    Takes the resulting segmentation and converts it to
    an image
    
    Attributes
    ----------
    threshold_tracker : ThresholdTracker
        Finds contours of the image
    binary_image_labeler : BinaryImageLabeler
        Finds connected components

    '''

    def __init__(self):
        '''
        Initializes the member variables
        '''
        self.threshold_tracker = ThresholdTracker()
        self.binary_image_labeler = BinaryImageLabeler()
        return

    def construct_image (self, partition):
        ''' 
        Reconstructs an image based upon graph cut output
 
        Displays and saves image


        Parameters
        ----------
        partition : nparray
            Result from Graph Cut

 
        '''

        masked_partition = self.mask_partition(partition)

        labeled_image = self.binary_image_labeler.label_binary_image(masked_partition)
        
        object_seeds = self.binary_image_labeler.extract_object_seeds(labeled_image)
        
        
        boundary_contours = self.threshold_tracker.trace_threshold(masked_partition)

        cleaned_contours = self.clean_contours(boundary_contours)
        self.draw_image(cleaned_contours)
        self.save_segmented_image(cleaned_contours)

    def draw_image(self, cleaned_contours):
        '''
        Draws image

        Parameters
        ----------
        cleaned_contours : nparray
            Processed graphcut output
        '''
        pylab.imshow(cleaned_contours)

    def save_segmented_image(self, cleaned_contours):
        '''
        Saves image

        Parameters
        ----------
        cleaned_contours : nparray
            Processed graphcut output
        '''
        pylab.imsave(cleaned_contours)

    def mask_partition (self, partition):
        '''
        Converts partition to binary graph
        
        Parameters
        ----------
        partition : nparray
            Graphcut output

        Returns
        -------
        nparray
             Binary valued matrix
        '''
        size = partition.shape()
        masked = np.zeros(size)
        for xxx in range (size[0]):
            for yyy in range (size[1]):
                if partition[xxx][yyy] > 0:
                    masked [xxx][yyy] = 1
        return masked

    def clean_contours(self, contours):
        '''
        Removes inner points from contours

        Parameters
        ----------
        contours : nparray
           Contours of segmentation
        '''
        for contour in (contours):
            for point in contour:
                if (self.is_point_inside(point.x, point.y, contour)):
                    contour[point] = 0


    def is_point_inside(self, xxx, yyy, point_array):
        '''
        Detects whether point is inside edge

        Parameters
        ----------
        xxx, yyy : int
            Coordinates of point
        point_array : nparray
            All points in image
        '''
        for iii in range (point_array.length):
            point_1 = point_array[iii]
            point_2 = point_array[iii-1]
            if (((point_1.y <= yyy and yyy <= point_2.y) or
                (point_2.y <= yyy and yyy <= point_1.y)) and
                ((point_1.x <= xxx and xxx <= point_2.x) or
                (point_2.x <= xxx and xxx <= point_1.x))):
                return True
        return False
            


