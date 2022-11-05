import numpy as np

def L1Norm(Dict1 , Dict2):
    P1 = np.array(Dict1.values)
    P2 = np.array(Dict2.values)
    
    Point1= np.array(normalize(P1))
    Point2 = np.array(normalize(P2))
    
    L1norm = numpy.linalg.norm((Point1 - Point2), ord=1)
    return L1norm
