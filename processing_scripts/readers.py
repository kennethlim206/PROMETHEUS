import os
import sys

# Reader for tasks and constructors
def task_reader(f):
	file = open(f, "r")
	lines = file.readlines()
	file.close()

	d = dict()
	d["PATH"] = f
	for l in lines:
		l = l.replace("\n", "")

		# Ignore commented out text
		if "#" in l:
			l = l.split("#")[0]

		# Parse <COMMAND> lines and input into dictionary
		if len(l) > 0:
			if l[0] == "<": 
				cmd_name = l[1:].split(">", 1)[0]
				cmd_val = l.split(">", 1)[1]

				if cmd_val[0] == " ":
					cmd_val = cmd_val.replace(" ", "", 1)

				d[cmd_name] = cmd_val
	return d

# Reader for function constructors
def constructor_reader(f):
	file = open(f, "r")
	lines = file.readlines()
	file.close()

	d = dict()
	d["PATH"] = f
	for i in range(0,len(lines)):
		l = lines[i]
		l = l.replace("\n", "")

		# Ignore commented out text
		if "#" in l:
			l = l.split("#")[0]

		# Parse <COMMAND> lines and input into dictionary
		if len(l) > 0:
			if l[0] == "<": 
				cmd_name = l[1:].split(">", 1)[0]
				cmd_val = l.split(">", 1)[1]

				# Sbatch script command spans multiple lines
				if cmd_name == "SCRIPT COMMAND":
					cmd_val = ""
					cmd_count = i + 1
					cmd_line = lines[cmd_count]

					while "}" not in cmd_line:
						cmd_val += cmd_line
						cmd_count += 1
						cmd_line = lines[cmd_count]

				if cmd_val[0] == " ":
					cmd_val = cmd_val.replace(" ", "", 1)

				d[cmd_name] = cmd_val
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
	for l in choose_lines:
		l = l.replace("\n", "")

		# Ignore commented out text
		if "#" in l:
			l = l.split("#")[0]

		# Parse <COMMAND> lines and input into dictionary
		if len(l) > 0:
			if l[0] == "<": 
				cmd_name = l[1:].split(">", 1)[0]

				cmd_val = l.split(">", 1)[1]
				cmd_val = cmd_val.replace(" ", "")

				d[cmd_name] = cmd_val
	return d




