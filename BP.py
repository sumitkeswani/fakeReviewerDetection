import csv
import numpy as np
import random
from sumproduct import Variable, Factor, FactorGraph


numOfFactors = 2	#distance only!
fileName = 'distances.csv'

# init Factor Graph
graph = FactorGraph(silent=False)

# variable map
reviewer2id = {}
id2reviewer = {}


current_id = 0
i=0
# load csv file
with open(fileName, 'rb') as f:
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
		temp1 = Variable(str(reviewer2id[reviewer1]), 2)
		temp2 = Variable(str(reviewer2id[reviewer2]), 2)
		common_prod = float(row[3])
		common_burst = float(row[4])
		dist = float(row[5])
		dist_fact_name = 'distf'+str(reviewer2id[reviewer1])+'_'+str(reviewer2id[reviewer2])
		dist_factor = Factor(dist_fact_name, np.array([[1-dist, dist],[dist, 1-dist]]))
		graph.add(dist_factor)
		graph.append(dist_fact_name, temp2)
		graph.append(dist_fact_name, temp1)
		print 'adding pair no:', i
		i+=1

num_of_reviewers = len(reviewer2id)
reviewers = list(reviewer2id.keys())
random.shuffle(reviewers)
reviewers = reviewers[:num_of_reviewers/5]

for i in reviewers:
	graph.observe(str(reviewer2id[i]), 2)

graph.compute_marginals(max_iter=500, tolerance=1e-4)

with open('output.csv', 'w') as f:
	for i in xrange(num_of_reviewers):
		output = str(i) + ', ' + id2reviewer[i] + ', ' + str(graph.nodes[str(i)].marginal()[0])
		f.write(output + '\n')

