'''

This test verifies that the  
Boundary Model is being generated 
correctly by the new code 

'''
import argparse
import numpy as np
from unittest import assertTrue
import matplotlib.image as mpimg

EPSILON = 1000


def compare_results(produced_output, expected_output):
    '''
    calculates the RMSE difference between the expected output
    and the produced output
    '''

    return ((produced_output.ravel()**2-expected_output.ravel()**2)/len(produced_output.ravel()))**0.5
         

def open_img(path):
    '''
    converts image to numpy array
    '''
    return mpimg.imread(path)


    
def run_test(inputs, background, foreground, target, modality, expected):
    '''
    the following function runs a test on the following inputs
    (1) input images
    (2) background seeds
    (3) foreground seeds
    (4) previous target data

    it runs the graphcut algorithm on these inputs.

    then the result is compared with the already-computed epected output
    '''

    boundary = []

    for input_img in (inputs):
        boundary = find_boundary_model (input_img, foreground, background, boundary, target)

    difference = compare_results (boundary, expected)
    return difference


def find_boundary_model (input_img, foreground, background, boundary, target):
    '''
    runs the graph cut algorithm on the image and 
    object/background seeds.
    '''
    return []

def main():
    '''
    takes from the command line the directory 
    where the input and expected output files are

    then it runs the test on the files and returns 
    a goodness-of-fit measurement.
    '''

    parser = argparse.ArgumentParser (description="Develops Training Data for Object Recognition")
    parser.add_argument("--inputs", 
                        "-i", 
                        dest="inputs",
                        required=True, nargs="+",
                    help="list of input images")
    parser.add_argument("--background",
                        "-b", 
                        dest="background",
                        required=True, nargs="1",
                        help="background image")
    parser.add_argument("--foreground", 
                        "-f", 
                        dest="foreground",
                        required=True, nargs="1",
                        help="foreground image")
    parser.add_argument("--modality", 
                        "-m", 
                        dest="modality",
                        required=True, nargs="1",
                        help="image modality")

    parser.add_argument("--target",
                        "-t", 
                        dest="target",
                        required=False, nargs="?",
                        help="Previous Target Training Data")

    parser.add_argument("--expected",
                        "-e", 
                        dest="expected",
                        required=True, nargs="1",
                        help="Expected Outcome")


    args = parser.parse_args()
    inputs = args.inputs
    foreground = args.foreground
    background = args.background
    modality = args.modality
    target = args.target
    boundary = args.boundary
    expected = args.expected
    epsilon = args.epsilon

    if (epsilon !=None):
        EPSILON=epsilon


    assertTrue( run_test(inputs, background, foreground, modality, target, expected) <= EPSILON)



if __name__ == '__main__':
    main()
