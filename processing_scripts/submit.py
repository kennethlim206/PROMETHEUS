import os
import sys
import commands
import datetime

test = 0

def shell_submit(shell_path, name, file_path):

	# Figure out test case vs. real case
	status = 0
	ID = "Submitting job as 1738"
	if not test:
		print "Submitting %s ..." % name
		status, ID = commands.getstatusoutput("sbatch %s" % shell)

	# Print out success or error message after cmd submit
	if status == 0:
		ID_split = ID.split(" ")
		ID = int(ID_split[3])
		print "Job %s submitted as %i" % (name, ID)
		print "Woot! Slurm will take it from here!"
	else:
		print "ERROR: SLUMR SAYS:\n%s" % ID
		print "-----------------"
		sys.exit()

	# Record job IDs
	file = open("%s/RED/sbatch_record.txt" % file_path, "a")

	file.write("Sumbitted on: %s\n" % datetime.datetime.now().strftime("%m.%d.%Y %H:%M:%S"))
	file.write("Job ID Number: %s\n" % ID)
	file.write("Submitted with command: %s\n" % cmd)
	file.write("-------------------------------\n\n")

	file.close()

	return ID