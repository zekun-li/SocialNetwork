import csv
import pickle
import matplotlib.pyplot as plt

worker_dict = {}


def createworker(workerid1, workerid2):
	global worker_dict 

	worker_dict[workerid1 + ' ' + workerid2] = {}
	worker_dict[workerid1 + ' ' + workerid2]['Number_Agreement'] = 0
	worker_dict[workerid1 + ' ' + workerid2]['Number_NotAgreement'] = 0

	return 0

f = open('Batch_2179946_batch_results.csv','rb')
csv_f = csv.reader(f)
next(csv_f)

for row in csv_f:
	worker1 = row[2]
	answer1 = row[3]

	worker2 = row[4]
	answer2 = row[5]
	
	agreement = True if row[6]== 'Yes' else False	

	if worker1 < worker2:
		if worker1+ ' ' + worker2 not in worker_dict:
			createworker(worker1,worker2)
		if agreement:
			worker_dict[worker1 + ' ' + worker2]['Number_Agreement'] +=1
		else:
			worker_dict[worker1 + ' ' + worker2]['Number_NotAgreement'] +=1

	else:
		if worker2+ ' ' + worker1 not in worker_dict:
			createworker(worker2,worker1)
		if agreement:
			worker_dict[worker2 + ' ' + worker1]['Number_Agreement'] +=1
		else:
			worker_dict[worker2 + ' ' + worker1]['Number_NotAgreement'] +=1

f = open('Batch_2179946_batch_results.csv','rb')
csv_f = csv.reader(f)
next(csv_f)
	
for row in csv_f:
	worker1 = row[2]
	answer1 = row[3]

	worker2 = row[4]
	answer2 = row[5]
	
	agreement = True if row[6]== 'Yes' else False	

	if worker1 < worker2:
		if worker1+ ' ' + worker2 not in worker_dict:
			createworker(worker1,worker2)
		if agreement:
			worker_dict[worker1 + ' ' + worker2]['Number_Agreement'] +=1
		else:
			worker_dict[worker1 + ' ' + worker2]['Number_NotAgreement'] +=1
	else:
		if worker2+ ' ' + worker1 not in worker_dict:
			createworker(worker2,worker1)
		if agreement:
			worker_dict[worker2 + ' ' + worker1]['Number_Agreement'] +=1
		else:
			worker_dict[worker2 + ' ' + worker1]['Number_NotAgreement'] +=1


print len(worker_dict)

worker_confidence = {}
for worker in worker_dict:
	worker_dict[worker]['total_count'] = worker_dict[worker]['Number_Agreement'] + worker_dict[worker]['Number_NotAgreement']
	worker_dict[worker]['confidence'] = worker_dict[worker]['Number_Agreement'] * 1.0 / worker_dict[worker]['total_count']
	worker_confidence[worker] = worker_dict[worker]['confidence']

for value,key in sorted([(value,key) for (key,value) in worker_confidence.items()],reverse = True):
	print value,key,worker_dict[key]['total_count']

