'''

This script generates the
Regional Object Model 

'''

import argparse
import matplotlib.image as mpimg
import pickle
import sys

def open_img(path):
    '''
    converts image to numpy array
    '''
    return mpimg.imread(path)


    
def create_object_model_from_series(
    input_images, sourcesink,  
    boundary_train=False, object_model=None):
    
    '''
    Finds the boundary model for a given set of images


    Attributes
    ----------
    input_images : Array[]
       Series of input images
    sourcesink : nparray
       Object pixels
    target :  nparray
       Background pixels
    modality : int
       Image Modality   
    boundary_train : bool
       Whether to train boundary
    object_model : pickled data
       Previously calculated object model


    Returns
    -------
    object_model : pickled data
      Object model

    '''
    if (object_model != None):
        final_model = pickle.load(object_model)

    for input_img in (input_images):
        final_model = create_object_model_from_image (
            input_img, sourcesink, boundary_train, final_model)
    return final_model



    
def create_object_model_from_image(
    input_image, sourcesink,  
    boundary_train=False, object_model=None):

    '''
    Finds the object model for a single input image


    Attributes
    ----------
    input_image : Array[]
       Single input image
    sourcesink : nparray
       Object pixels
    target :  nparray
       Background pixels
    modality : int
       Image Modality   
    boundary_train : bool
       Whether to train boundary
    object_model : pickled data
       Previously calculated object model


    Returns
    -------
    object_model : pickled data
      Object model
    '''
    return []

def main():
    '''
    Produces the object model of a 
    series of images based on 
    from the command line

    '''


    parser = argparse.ArgumentParser (
        description="Develops Training Data \
                     for Object Recognition")
    parser.add_argument("--inputs", 
                        "-i", 
                        dest="inputs",
                        required=True, nargs="+",
                    help="List of input images")
    parser.add_argument("--sourcesink",
                        "-s", 
                        dest="sourcesink",
                        required=True, nargs="1",
                        help="Sourcesink pixels")
    parser.add_argument("--boundary", 
                        "-b", 
                        dest="boundary",
                        required=False, nargs="0",
                        help="Train boundary")
    parser.add_argument("--Model",
                        "-M", 
                        dest="Model",
                        required=False, nargs="?",
                        help="Previous boundary model datafile")
    parser.add_argument("--output", 
                        "-o", 
                        dest="output",
                        required=True, nargs="1",
                        help="Output File")


    args = parser.parse_args()
    inputs = args.inputs
    sourcesink = args.sourcesink
    boundary = args.boundary
    model = args.Model
    output = args.output


    output_file = open(output, 'w+')
    pickle.dump(create_object_model_from_series(
        inputs, sourcesink, boundary, model), output_file)
        

if __name__ == '__main__':
    main()
