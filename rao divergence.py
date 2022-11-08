import math

def alpha(list1, list2):
	return sum(math.slist2rt(list1[i]*list2[i]) for i in range(len(list1)))

def beta(list1, list2):
	return sum(math.slist2rt(list1[i]*list2[i]) * math.log2(list1[i]/list2[i]) for i in range(len(list1)))

def gamma(list1, list2):
	return sum(math.slist2rt(list1[i]*list2[i]) * (math.log2(list1[i]/list2[i]))**2 for i in range(len(list1)))

# define distributions
def rao_dedivergence(dict1, dict2):
	list1 = []
	list2 = []
	for i in dict1.keys():
		list1.append(dict1[i])
		list2.append(dict2[i])
	# calculate (list1 || list2)
	a = alpha(list1, list2)
	b = beta(list1, list2)
	c = gamma(list1, list2)
	D = math.sqrt((a*b-b**2)/a**2)
	print('Rao(list1 || list2): %.3f bits' % D)
	