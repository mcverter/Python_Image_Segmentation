'''
The image slice offers up a view of the image that 
allows one to access the value of the various 
intensity values of the grayscale image.
One can also access the locations of the object and
background seeds
'''

import numpy as np

SINK = -1
SOURCE = 1

class ImageInterface(object):
    '''
    The image slice offers up a view of the image that 
    allows one to access the value of the various 
    intensity values of the grayscale image.
    One can also access the locations of the object and
    background seeds

    It is initialized with the various grayscale values 
    of the various pixels.  Then it is imprinted with 
    the image features of the source and the sink

    Attributes
    ----------
    image_array : nparray
         Array of image intensity values
    seed_array  : nparray
         Array of source and sink flags
    '''

    def __init__(self, image_array):
        ''' 
        Initializes member variables
        '''
        self.image_array = []
        self.seed_array = []

    def add_object_seed (self, xxx, yyy):
        ''' 
        Marks the pixel as being an object seed

        Parameters 
        ----------
        xxx, yyy : int
            Pixel coordinates
        '''
        self.seed_array[xxx][yyy] = SOURCE


    def add_background_seed (self, xxx, yyy):
        ''' 
        Marks the pixel as being a background seed

        Parameters 
        ----------
        xxx, yyy : int
            Pixel coordinates
        '''
        self.seed_array[xxx][yyy] = SINK


    def get_observation(self, xxx, yyy):
        ''' 
        Gets the pixel value at the given coordinates 

        Parameters 
        ----------
        xxx, yyy : int
            Pixel coordinates

        Returns
        -------
        float 
           Intensity value
        '''
        return self.image_array[xxx][yyy]

    def is_object_seed(self, xxx, yyy):
        '''
        Indicates whether the pixel contains object seed

        Parameters 
        ----------
        xxx, yyy : int
            Pixel coordinates

        Returns
        -------
        bool
            Whether pixel contains object seed
        '''
        return self.seed_array[xxx][yyy] == SOURCE

    def is_background_seed(self, xxx, yyy):
        '''
        Indicates whether the pixel contains object seed  

        Parameters 
        ----------
        xxx, yyy : int
            Pixel coordinates

        Returns
        -------
        bool
            Whether pixel contains background seed

        '''
        return self.seed_array[xxx][yyy] == SINK

    def get_neighbor_pixels (self, xxx, yyy):
        '''
        Gets neighboring pixels

        Parameters 
        ----------
        xxx, yyy : int
            Pixel coordinates

        Returns
        -------
        list 
           List of neighboring pixels
        '''
        # assume 4 connection for now
        neighbors = []
        if (xxx > 0):
            neighbors.append(self.image_array[xxx-1][yyy])
        if (yyy > 0):
            neighbors.append(self.image_array[xxx][yyy-1])
        if (xxx < self.image_array.width-2):
            neighbors.append(self.image_array[xxx+1][yyy])
        if (xxx < self.image_array.height-2):
            neighbors.append(self.image_array[xxx][yyy+1])
        return self.image_array[xxx][yyy]

