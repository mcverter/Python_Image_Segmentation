'''
This script unit tests the various Command Line Scripts


'''
import re
import unittest
from subprocess import Popen
import pickle
import matplotlib.image as mpimg

EPSILON = 1000
EPSILON = 1000

def checkForError(errorlog):
    '''
    parses the stderr to make sure there is no error
    '''
    f = open(errorlog, 'r+')
    if (re.search("rror", errorlog.read()) == None):
        return False
    else:
        return True

def compare_images (produced_output, expected_output):
    '''
    calculates the RMSE difference between the expected 
    image and the produced output

    Used to compare two segmentations

    This function might not be necessary because
    we can easily convert the image in UnitTest::set_up.

    However, there might be fundamental differences 
    in the way we compare PKL files and IMG files.
    '''
    p = open(produced_output, 'r+')
    e = open(expected_output, 'r+')
    produced_array = mpimg.imread(p.read())
    expected_array = mpimg.imread(e.read())
    return compare_results(produced_output, expected_array)

def compare_results(produced_output, expected_output):
    '''
    calculates the RMSE difference between the 
    expected output and the produced output

    Used to compare two pkl files in boundary or saass tests
    '''
    
    return ((produced_output.ravel()**2-expected_output.ravel()**2)/len(produced_output.ravel()))**0.5



class TestTrainingData(unittest.TestCase):
    def set_up(self):
        self.expected = "expected_fore_back_1.pkl"
        self.error_log = "errlog.txt"
        self.output_name = "test_training_data.pkl"
        


    def run_test(self):
        pid = Popen("saass_train.py  -i CT_slice.png MR_slice.png -s source_sink_mask.png -o " + self.output_name, shell=True, stderr=self.error_log)
        pid.communicate()
        self.assertTrue(checkForError(self.error_log )==False)
        self.assertLessEqual(compare_results(self.output_name, self.expected), EPSILON)

        
class TestSegmentation(unittest.TestCase):
    def set_up(self):
        self.expected = "expected_segmentation_1.png"
        self.error_log = "errlog.txt"
        self.output_name = "test_segmentation.png"

    def run_test(self):
        pid = Popen("segment_image.py  -i CT_slice.png MR_slice.png -M background_foreground_values_1.pkl -o " + self.output_name, shell=True, stderr=self.error_log)
        self.assertTrue(checkForError(self.error_log)==False)
        self.assertLessEqual(compare_image(self.output_name, self.expected), EPSILON)

class TestBoundary(unittest.TestCase):

    def set_up(self):
        self.expected = pickle.load("expected_fore_back_boundary_2.pkl")
        self.error_log = "errlog.txt"
        self.output_name = "test_boundary.pkl"


    def run_test(self):
        pid = Popen("saass_train.py  -i CT_slice.png MR_slice.png -s source_sink_mask_2.png -b -o " self.output_name, shell=True, stderr=self.error_log)
        (stdoutdata, stderrdata) = pid.communicate()
        self.assertTrue(checkForError(self.error_log)==False)
        self.assertLessEqual(compare_results(self.output_name, self.expected), EPSILON)



class TestSegmentationNoTraining(unittest.TestCase):
    def set_up(self):
        self.expected = expected_segmentation_2.png
        self.error_log = "errlog.txt"
        self.output_name = "test_segmentation_no_training.png"


    def run_test(self):
        pid = Popen("segment_image.py  -i CT_slice.png MR_slice.png -M background_foreground_boundary_samples2.pkl -o " + self.output_name, shell=True, stderr=self.error_log)
        self.assertTrue(checkForError(self.error_log)==False)
        self.assertLessEqual(compare_image(self.output_name, self.expected), EPSILON)

