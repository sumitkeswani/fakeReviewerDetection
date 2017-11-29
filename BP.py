import csv
import numpy as np
from sumproduct import Variable, Factor, FactorGraph

numOfFactors = 1	#distance only!
fileName = 'electronics.csv'

# init Factor Graph
graph = FactorGraph(silent=False)

# variable map
reviewer2id = {}
id2reviewer = {}

# reviewer array
reviewers = []

current_id = 0
i=0
# load csv file
with open(, 'rb') as f:
	data = csv.reader(f, delimiter=',')
	for row in data:
		reviewer1 = row[1]
		reviewer2 = row[2]
		if(reviewer1 not in reviewer2id):
			reviewer2id[reviewer1] = current_id
			id2reviewer[current_id] = reviewer1
			current_id += 1
		if(reviewer2 not in reviewer2id):
			reviewer2id[reviewer2] = current_id
			id2reviewer[current_id] = reviewer2
			current_id += 1

		temp1 = Variable(reviewer2id[reviewer1], 1)
		temp2 = Variable(reviewer2id[reviewer2], 1)

		common_prod = float(row[3])
		common_burst = float(row[4])
		dist = float(row[5])
		dist_fact_name = 'distf'+str(reviewer2id[reviewer1])+'_'+str(reviewer2id[reviewer2])
		dist_factor = Factor(dist_fact_name, np.array([[dist]]))
		graph.add(dist_factor)
		graph.append(dist_fact_name, temp1)
		graph.append(dist_fact_name, temp2)
		print 'adding pair no:', i
		i+=1

graph.compute_marginals()

