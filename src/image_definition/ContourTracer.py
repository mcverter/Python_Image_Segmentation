''' 
The contour tracer is responsible for 
determining a set of contours for an image.

Given a 2D array of points, it analyses these points 
and returns a set of contours for the image.
'''
import numpy as np

class ContourTracer(object):
    ''' 
    The contour tracer is responsible for 
    determining a set of contours for an image.
    
    Given a 2D array of points, it analyses these points 
    and returns a set of contours for the image.

    Attributes
    ----------
    image : nparray
        Image being analyzed
    mask  : nparray
        Image with defined contours

    xnow, ynow : int
        Indexes of pixel being analyzed
    '''
    def __init__(self):
   
        '''
        Initializes all member variables to null values
        '''
        self.image = np.zeros(1)
        self.mask = np.zeros(1)
        self.xnow = -1
        self.ynow = -1


    def trace_contours(self):
        '''
        Traces the contours of the given image

        Returns 
        -------
        nparray
            A set of contour points
        '''

        contour_points = []
        while (self.get_start):
            contour = self.get_contour_point()
            if(contour != None):
                contour_points.append(contour)
        return contour_points

    def get_start(self):
        '''
        Gets the next possible start for contour point search

        Returns
        -------
        bool
           Whether a contour point search could be started

        int, int
           Sets the global xnow, ynow coordinates of the point
        '''
        for xxx in range (self.image.width):
            for yyy in range (self.image.height):
                if (self.is_point_on_boundary(xxx, yyy)):
                    xnow = xxx
                    ynow = yyy
                    return True
        return False
                    
                    
    def is_point_on_boundary(self, xxx,  yyy):
        '''
        Determines whether point is already within other points


        Parameters
        ----------
        xxx, yyy : int 
             Coordinates of point

        Returns
        -------
        bool
            Whether point is on boundary or not
        '''
        if (xxx == 0 or yyy == 0 or xxx == self.image.width - 1 or yyy == self.image.height -1):
            return False
        if (self.image[xxx][yyy]==0 and self.mask[xxx][yyy]==0):
            if (self.image[xxx+1][yyy] !=0 or
                self.image[xxx-1][yyy] !=0 or
                self.image[xxx][yyy+1] !=0 or
                self.image[xxx+1][yyy-1] !=0):
                return True
        return False

    def get_contour_point (self):
        '''
        Finds next contour point

        Returns
        -------
        bool
           Whether a contour point search could be started

        int, int
           Sets the global xnow, ynow coordinates of the point
        '''
        xxx = self.xnow
        yyy = self.ynow
        x_r = self.xnow + 1
        x_l = self.xnow - 1
        y_u = self.ynow - 1
        y_d = self.ynow + 1

        if (self.is_point_on_boundary(x_r, self.ynow)):
            self.xnow = x_r
            return True
        if (self.is_point_on_boundary(x_r, y_u)):
            self.xnow = x_r
            self.ynow = y_u
            return True
        if (self.is_point_on_boundary(x_l, self.ynow)):
            self.xnow = x_l
            return True
        if (self.is_point_on_boundary(x_l, y_u)):
            self.xnow = x_l
            self.ynow = y_u
            return True

        if (self.is_point_on_boundary(x_r, y_d)):
            self.xnow = x_r
            self.ynow = y_d
            return True
        if (self.is_point_on_boundary(x_l, y_d)):
            self.xnow = x_l
            self.ynow = y_d
            return True

        if (self.is_point_on_boundary(self.xnow, y_u)):
            self.ynow = y_u
            return True
        if (self.is_point_on_boundary(self.xnow, y_d)):
            self.ynow = y_d
            return True
        return False
        



