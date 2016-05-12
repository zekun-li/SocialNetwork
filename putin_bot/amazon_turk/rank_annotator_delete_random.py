import csv
import pickle
import matplotlib.pyplot as plt

bad_list=['AHPOH7GFQK14J','AFIIFNK4FM7MZ','A1S88VQY8G8CNC','A2LV5QYHH24OMY','A2ZBYVQLDUZOV7','A1DRFDGG2KCOI2','A2S96ZZ70YFPSK', 'A3J2UG22S8BIW4','A1NJ1IJLKAS0Y4','A1012N48J0Z65N','AP2HL1DHHBIC6','A23WTODPHXZ68Y','ANBP9PU6EH8DB','A39FH0T1NKKMVO','A1E6RS45GUAFC3','AZD9Z5B2U40G2','AVX3SWFMBEPMZ', 'AMAAE4PQGWD99','A3KOVCQYR8K3HY','A2W2ZEI7WUASOW','A2R33BOX381SD3','A2FCGEU5RTEWG8','A2C0QNEIOSKAV5','A2BO8M77CS3SGZ','A28PS7TGEQCFT4','A1RH7GXPE8K2O6','A1NP3XGUAKE96X']
worker_dict = {}


def createworker(workerid):
	global worker_dict 
	worker_dict[workerid] = {}
	worker_dict[workerid]['Number_Pro-Putin'] = 0
	worker_dict[workerid]['Number_Anti-Putin'] = 0
	worker_dict[workerid]['Number_Cannot_Judge'] = 0
	worker_dict[workerid]['Number_Agreement'] = 0
	worker_dict[workerid]['Number_NotAgreement'] = 0

	return 0

f = open('Batch_2179946_batch_results.csv','rb')
csv_f = csv.reader(f)
next(csv_f)

for row in csv_f:
	worker1 = row[2]
	answer1 = row[3]

	worker2 = row[4]
	answer2 = row[5]

	if worker1 in bad_list or worker2 in bad_list:
		continue
	
	agreement = True if row[6]== 'Yes' else False	

	if worker1 not in worker_dict:
		createworker(worker1)
	if worker2 not in worker_dict:
		createworker(worker2)

	if answer1 == 'Pro-Putin':
		worker_dict[worker1]['Number_Pro-Putin'] +=1
	elif answer1 == 'Anti-Putin':
		worker_dict[worker1]['Number_Anti-Putin'] +=1
	else:
		worker_dict[worker1]['Number_Cannot_Judge'] +=1

	if answer2 == 'Pro-Putin':
		worker_dict[worker2]['Number_Pro-Putin'] +=1
	elif answer2 == 'Anti-Putin':
		worker_dict[worker2]['Number_Anti-Putin'] +=1
	else:
		worker_dict[worker2]['Number_Cannot_Judge'] +=1

	if agreement:
		worker_dict[worker1]['Number_Agreement'] +=1
		worker_dict[worker2]['Number_Agreement'] +=1
	else:
		worker_dict[worker1]['Number_NotAgreement'] +=1
		worker_dict[worker2]['Number_NotAgreement'] +=1


f = open('Batch_2180675_batch_results.csv','rb')
csv_f = csv.reader(f)
next(csv_f)

for row in csv_f:
	worker1 = row[2]
	answer1 = row[3]

	worker2 = row[4]
	answer2 = row[5]
	
	if worker1 in bad_list or worker2 in bad_list:
		continue

	agreement = True if row[6]== 'Yes' else False	

	if worker1 not in worker_dict:
		createworker(worker1)
	if worker2 not in worker_dict:
		createworker(worker2)

	if answer1 == 'Pro-Putin':
		worker_dict[worker1]['Number_Pro-Putin'] +=1
	elif answer1 == 'Anti-Putin':
		worker_dict[worker1]['Number_Anti-Putin'] +=1
	else:
		worker_dict[worker1]['Number_Cannot_Judge'] +=1

	if answer2 == 'Pro-Putin':
		worker_dict[worker2]['Number_Pro-Putin'] +=1
	elif answer2 == 'Anti-Putin':
		worker_dict[worker2]['Number_Anti-Putin'] +=1
	else:
		worker_dict[worker2]['Number_Cannot_Judge'] +=1

	if agreement:
		worker_dict[worker1]['Number_Agreement'] +=1
		worker_dict[worker2]['Number_Agreement'] +=1
	else:
		worker_dict[worker1]['Number_NotAgreement'] +=1
		worker_dict[worker2]['Number_NotAgreement'] +=1

print len(worker_dict)

worker_confidence = {}
for worker in worker_dict:
	worker_dict[worker]['total_count'] = worker_dict[worker]['Number_Agreement'] + worker_dict[worker]['Number_NotAgreement']
	worker_dict[worker]['confidence'] = worker_dict[worker]['Number_Agreement'] * 1.0 / worker_dict[worker]['total_count']
	worker_confidence[worker] = worker_dict[worker]['confidence']

data = []
for value,key in sorted([(value,key) for (key,value) in worker_confidence.items()],reverse = True):
	print value,key,worker_dict[key]['total_count']
	for i in range(worker_dict[key]['total_count']):
		data.append(value)

plt.hist(data,100)
plt.xlabel("Confodence")
plt.ylabel("Count")

plt.show()
