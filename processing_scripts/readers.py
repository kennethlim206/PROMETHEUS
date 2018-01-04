import os
import sys

# Reader for tasks and constructors
def default_reader(f):
	file = open(f, "r")
	d = dict()

	for line in file:
		line = line.replace("\n", "")

		# Ignore commented out text
		if "#" in line:
			line = line.split("#")[0]

		# Parse <COMMAND> lines and input into dictionary
		if len(line) > 0:
			if line[0] == "<": 
				task_name = line[1:].split(">", 1)[0]
				task_val = line.split(">", 1)[1]

				if task_val[0] == " ":
					task_val = task_val.replace(" ", "", 1)


				d[task_name] = task_val

	file.close()
	return d

# Reader for special genome table files
def genome_reader(f, ID):

	# Error check for blank ID
	if ID == "":
		sys.exit("ERROR: <REF ID> has not been chosen and is required to run your chosen action.")

	file = open(f, "r")
	lines = file.readlines()
	file.close()

	# Find specific lines under <REF ID>
	choose_lines = []
	for i in range(0,len(lines)):
		if "<REF ID> %s" % ID in lines[i]:
			choose_lines.append(lines[i])
			choose_lines.append(lines[i+1])
			choose_lines.append(lines[i+2])
			choose_lines.append(lines[i+3])
			break

	d = dict()
	for line in choose_lines:
		line = line.replace("\n", "")

		# Ignore commented out text
		if "#" in line:
			line = line.split("#")[0]

		# Parse <COMMAND> lines and input into dictionary
		if len(line) > 0:
			if line[0] == "<": 
				task_name = line[1:].split(">", 1)[0]

				task_val = line.split(">", 1)[1]
				task_val = task_val.replace(" ", "")

				d[task_name] = task_val
	return d




