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

	sbatch_scripts = tools.get_other(SCR, ".sh")

	print ""
	print " SUBMISSION SCRIPTS:"
	print " ------------------------------------------------------------------------------- "

	for full_path in sbatch_scripts:
		print " %s" % full_path.rsplit("/", 1)[1]

	done = False
	while not done:

		print ""
		print " Note: Resubmitting is for individual script failture. If all jobs failed, consider using the 'submit' option instead."
		print " The existing sbatch output and error files will be archived and replaced with the resubmitted versions."
		print ""
		print " ------------------------------------------------------------------------------- "
		print " Input the name of the selected script below, or type 'done' to return to Step 2."
		print ""

		selected_script = raw_input(" >>> ")

		if selected_script == "done":
			done = True

		else:
			selected_script_path = "%s/%s" % (SCR, selected_script)

			if not os.path.isfile(selected_script_path):
				sys.exit(" ERROR: You have chosen a script name that does not exist: %s" % selected_script)



		

	



	

	

if __name__ == '__main__':
	main()


