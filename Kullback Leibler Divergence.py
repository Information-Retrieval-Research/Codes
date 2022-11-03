import numpy as np
  

def kl_divergence(dict1, dict2):
  '''
  This function needs two hashmap which have to be converted to their probabilities.
  '''
  list1 = []
  list2 = []
  for i in dict1.keys():
    list1.append(dict1[i])
    list2.append(dict2[i])

  return sum(list1[i]*np.log(list1[i]/list2[i]) for i in range(len(list1)))