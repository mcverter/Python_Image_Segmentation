''' 
The threshold tracker is responsible for 
determining a set of threshold points for an image.

Given a 2D array of points, it analyses these points 
and returns a set of threshold points for the image.
'''

import numpy as np

DIRECTIONS = [ [1, 0], [1, -1],  [0, -1],  [-1, -1], [-1, 0], [-1, 1],  [0, 1],  [1, 1] ]

class ThresholdTracker(object): 
    '''
    The threshold tracker is responsible for 
    determining a set of threshold points for an image.

    Given a 2D array of points, it analyses these points 
    and returns a set of threshold points for the image.

    The Threshold Tracker implements the following algorithm:
    (1)Scan the image from left to right and from
       top to bottom until an 1 pixel is found
    (2) stop if this is the initial pixel
    (3) if it is 1, add it to the boundary
    (4) go to a 0 4-neighbor on its left
    (5) check the 8-neighbors of the current pixel and
        go to the first 1 pixel found in clockwise order
    (6) go to step (2)

    Attributes
    ----------
    image : nparray
        Image being analyzed
    mask  : nparray
        Image with defined contours

    x_tt, y_tt : int
        Indexes of pixel being analyzed

    '''
    def __init__(self):
        '''
        Initializes the member values
        '''
        self.image = np.zeros(1)
        self.mask = np.zeros(1)
        self.x_tt = 0
        self.x_yy = 0
        
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
        if ((self.image[xxx][yyy]!=0 and self.image[xxx-1][yyy] and self.mask[xxx][yyy]==0) or  
            self.image[xxx+1][yyy] !=0 or
            self.image[xxx-1][yyy] !=0 or
            self.image[xxx][yyy+1] !=0 or
            self.image[xxx+1][yyy-1] !=0):
            return True
        return False

 
    
    def get_start(self):
        '''
        Gets the next possible start for threshold point search

        Returns
        -------
        bool
           Whether a threshold point search could be started

        int, int
           Sets the global x_tt, y_tt coordinates of the point
        '''
        for xxx in range (self.image.width):
            for yyy in range (self.image.height):
                if (self.is_point_on_boundary(xxx, yyy)):
                    self.x_tt = xxx
                    self.y_tt = yyy
                    return True
        return False
        
    def trace_threshold (self):
        '''
        Traces the threshold of the given image

        Returns 
        -------
        nparray
            A set of threshold points
        '''
        contours = []
        while (self.get_start()):
            self.init_tt(self.x_tt, self.y_tt)
            current_contour = []
            while(self.next_point()):
                if (current_contour.length > 3):
                    if (current_contour[0].x == current_contour[length-1].x and current_contour[0].y == current_contour[length-1].y):
                        break
            contours.append(current_contour)
        return contours

    def next_point(self):
        '''
        Finds next threshold point

        Returns
        -------
        bool
           Whether a threshold point  could be found

        int, int
           Sets the global x_tt, y_tt coordinates of the point
        '''

        curr_dir = 0
        xxx = self.x_tt
        yyy = self.y_tt
        for iii in range (8):
            dirr = (iii + curr_dir) % 8
            txx = self.x_tt + DIRECTIONS[dirr][0]
            tyy = self.y_tt + DIRECTIONS[dirr][1]
            if self.image[txx][tyy]:
                self.x_tt = txx
                self.y_tt = tyy
                curr_dir = (dirr+6) % 8
                return True
        return False


    def init_tt(self, xxx, yyy):
        '''
        Initializes the direction of the threshold search

        Parameters
        ----------
        xxx, yyy : int 
             Coordinates of point

        Returns
        -------
        bool 
            Whether a search direction could be found
        '''
        self.x_tt = xxx
        self.y_tt = yyy
        for curr_dir in range (8):
            cx = self.x_tt + DIRECTIONS[curr_dir][0]
            cy = self.y_tt + DIRECTIONS[curr_dir][1]
            nx = self.x_tt + DIRECTIONS[next_dir][0]
            ny = self.x_tt + DIRECTIONS[next_dir][1]

            if ((cx >= 0) and (cx < self.image.width) and
                (cy >= 0) and (cy < self.image.heigth)and
                (self.image[cx][cy] == 0)  and (self.image[nx][ny]!= 0)):
                return True
        return False

