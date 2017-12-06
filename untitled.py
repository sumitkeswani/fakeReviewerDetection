import csv


file1 = "./raw_data.tsv"
file2 = "./output.csv"

reviewerprob = {}

with open(file2, 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
		prob = float(row[2])
		if prob <= 0.45:
			reviewerprob[row[1].strip()] = prob


monthfreq = {}
monthfreq[1] = 0
monthfreq[2] = 0
monthfreq[3] = 0
monthfreq[4] = 0
monthfreq[5] = 0
monthfreq[6] = 0
monthfreq[7] = 0
monthfreq[8] = 0
monthfreq[9] = 0
monthfreq[10] = 0
monthfreq[11] = 0
monthfreq[12] = 0

with open(file1, 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter='\t')
	for row in spamreader:
		reviewerid = row[1].strip()
		# print reviewerid
		if reviewerid in reviewerprob:
			print "in"
			date = row[8].strip()
			month = int(date[0:2])
			year = int(date[-4:])
			if (year > 2000 and year <= 2010):
				monthfreq[month] += 1



print monthfreq