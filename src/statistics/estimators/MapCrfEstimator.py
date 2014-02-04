'''
The MAP CRF Estimator produces regional and boundary 
estimates for the graph cut using the 
Maximum a Prioris and Conditional Random Fields
'''


from NonParametricEstimator import NonParametricProbabilityDensityEstimator

class MapCrfEstimator (object):
    '''
    The MAP CRF Estimator produces regional and boundary 
    estimates for the graph cut using the 
    Maximum a Prioris and Conditional Random Fields

    Attributes
    ----------
    source_estimator : NonParametricProbabilityDensityEstimator
       For estimating the object region
    sink_estimator : NonParametricProbabilityDensityEstimator
       For estimating the background region
    boundary_estimator : NonParametricProbabilityDensityEstimator
       For estimating the  the boundary between the two
    '''

    def __init__(self):
        '''
        Initializes member variables to empty values
        '''
        self.source_estimator = NonParametricProbabilityDensityEstimator()
        self.sink_estimator = NonParametricProbabilityDensityEstimator
        self.boundary_estimator = NonParametricProbabilityDensityEstimator
        
    def initialize(self, source_estimator, sink_estimator, boundary_estimator):
        '''
        Initializes member variables with existing estimators

        Parameters
        ----------
        source_estimator : NonParametricProbabilityDensityEstimator
            For estimating the object region
        sink_estimator : NonParametricProbabilityDensityEstimator
            For estimating the background region
        boundary_estimator : NonParametricProbabilityDensityEstimator
            For estimating the  the boundary between the two
        '''
        self.source_estimator = source_estimator
        self.sink_estimator =  sink_estimator
        self.boundary_estimator =  boundary_estimator

    def get_boundary(self, features_1, features_2):
        '''
        
        Estimates the likelihood of a boundary occuring between two features

        Parameters
        ----------
        feature_1, feature_2 : float
           Values of two adjacent features


        Returns
        -------
        float :
            Probability that there is a boundary
        '''
        merged_features = features_1.clone()
        merged_features.append(features_2)
        return self.boundary_estimator.estimate(merged_features)

    def  estimate_source_region(self, feature):
        '''
        Estimates feature's likelihood of belonging to the source
        Parameters
        ----------
        feature : float
           Value feature


        Returns
        -------
        float :
            Probability that it belongs to the source region
        '''
        return self.source_estimator.estimate(feature)
    
    def  estimate_sink_region(self, feature):
        '''
        Estimates the feature's possiblity of belonging to the sink region
  
        Parameters
        ----------
        feature : float
           Value feature


        Returns
        -------
        float :
            Probability that it belongs to the source region
        '''
        return self.sink_estimator.estimate(feature)


    def set_sink_estimator(self, estimator):
        '''
        Initializes the sink region estimator 

        Parameters
        ----------
        sink_estimator : NonParametricProbabilityDensityEstimator
            For estimating the background region
        '''

        self.sink_estimator = estimator

    def set_source_estimator(self, estimator):
        '''
        Initializes the source region estimator

        Parameters
        ----------
        source_estimator : NonParametricProbabilityDensityEstimator
            For estimating the object region
        '''
        self.source_estimator = estimator
