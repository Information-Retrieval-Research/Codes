import numpy as np

def L2Norm(Dict1 , Dict2):
    P1 = np.array(Dict1.values)
    P2 = np.array(Dict2.values)
    
    Point1= np.array(normalize(P1))
    Point2 = np.array(normalize(P2))
    
    L2norm = numpy.linalg.norm((Point1 - Point2), ord=2)
    return L2norm

