import os
import sys
import imp
import commands
from datetime import datetime

def main(t,f):

	# Import processing modules
	tools = imp.load_source("tools", "./processing_scripts/burst_tools.py")

	# Load task info from reader
	td = tools.task_reader(t)
	cd = tools.function_reader(f)

	LOOKUP_DIR = ""
	if cd["OUTPUT DIR"] == "RAW":
		LOOKUP_DIR = td["RAW DATA DIR"]
	elif cd["OUTPUT DIR"] == "INDEX":
		LOOKUP_DIR = td["INDEX DIR"]

	elif "POST:" in cd["OUTPUT DIR"]:
		LOOKUP_DIR = "%s/%s" % (td["POST DIR"], cd["OUTPUT DIR"].split(":")[1])

	else:
		sys.exit(" ERROR: Incorrect input into <OUTPUT DIR> command in function constructor.")

	# Get job_ids, output and error file summary from RED
	if not os.path.isdir(LOOKUP_DIR):
		sys.exit(" ERROR: The following directory doesn't exist: %s" % LOOKUP_DIR)

	RED = "%s/RED" % LOOKUP_DIR

	if not os.path.isdir(RED):
		sys.exit(" ERROR: You have chosen a directory that does not contain a RED: %s" % LOOKUP_DIR)

	# Base progress report on submission record (anything downstream could have been cancelled)
	OUT = "%s/sbatch_output" % RED
	ERR = "%s/sbatch_error" % RED
	SCR = "%s/sbatch_scripts" % RED
	SUB = "%s/submission_record.txt" % RED

	if not os.path.isfile(SUB):
		sys.exit(" ERROR: You have chosen a directory that does not contain a submission record: %s" % RED)

	for script in SCR:
		print script

	

	

if __name__ == '__main__':
	main()


