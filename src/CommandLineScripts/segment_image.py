'''

This script creates a segmentation

'''

import argparse
import matplotlib.image as mpimg


def open_img(path):
    '''
    converts image to numpy array
    '''
    return mpimg.imread(path)


    
def create_segmentation(
    input_channels, sourcesink, 
    modality, boundary_train=False, object_model=None):

    '''
    Creates a segmentation of a set of images.


    Attributes
    ----------
    input_channels : Array[]
       Various dimensions of input image
    source : nparray
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
    nparray :
        Segmented_Image

    '''

    return []



def main():
    '''
    Produces a segmentation of an image
    from the command-line parameters
    '''

    parser = argparse.ArgumentParser (description="Create segmentation from image dimensions and source and target seeds")
    parser.add_argument("--inputs", 
                        "-i", 
                        dest="inputs",
                        required=True, nargs="+",
                    help="List of input dimensions")
    parser.add_argument("--sourcesink",
                        "-s", 
                        dest="sourcesink",
                        required=True, nargs="1",
                        help="Source pixels")
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
    output_file.write ((create_segmentation(
                inputs, sourcesink, boundary, model)))

        

if __name__ == '__main__':
    main()

