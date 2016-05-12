import sys

old_file = open('guardian_urls.txt','r')
new_file = open('guardian_updated_url.txt','r')

list = []
for line in old_file:
	list.append(line.strip())

counter = 0
for line in new_file:
	if line.strip() not in list:
		print line.strip()
		counter += 1

print counter
