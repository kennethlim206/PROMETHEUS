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

	chosen = False

	while not chosen:
		if cd["AUTO CALL"] == "":
			chosen = True
		else:
			auto_cd = tools.function_reader("./user_function_constructors/%s" % cd["AUTO CALL"])

			if auto_cd["OUTPUT DIR"] == cd["OUTPUT DIR"]:
				chosen = True
			else:
				print ""
				print " Your selected function has an auto-called function with data stored in a different directory."
				print " Please select one to view:"
				print " %s" % cd["FUNCTION NAME"]
				print " %s" % auto_cd["FUNCTION NAME"]
				print ""

				new_f = raw_input(" >>> ")

				if new_f == auto_cd["FUNCTION NAME"]:
					cd = auto_cd
				elif new_f == cd["FUNCTION NAME"]:
					chosen = True
				else:
					sys.exit(" ERROR: Incorrect input. Please select one of the given functions.")

	LOOKUP_DIR = ""
	if cd["OUTPUT DIR"] == "RAW":
		LOOKUP_DIR = td["RAW DATA DIR"]
	elif cd["OUTPUT DIR"] == "INDEX":
		LOOKUP_DIR = td["INDEX DIR"]

	elif "POST:" in cd["OUTPUT DIR"]:
		LOOKUP_DIR = "%s/%s" % (td["POST DIR"], cd["OUTPUT DIR"].split(":")[1])

	else:
		sys.exit(" ERROR: Incorrect input into <OUTPUT> command in function constructor.")

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

	# Get job IDs and names
	file = open(SUB, "r")
	ID_LT = dict()

	for line in file:
		line = line.replace("\n", "")

		if line != "" and "\t" in line:
			data = line.split("\t")

			path = data[1]
			name = path.rsplit("/", 1)[1]
			ID = data[2]

			ID_LT[int(ID)] = name

	file.close()

	# STEP 1: LIVE REPORT
	expired = False

	# Get job submission time
	submit_time = commands.getoutput("grep '<SUBMITTED>' %s" % SUB)
	submit_time = submit_time.split("<SUBMITTED> ")[1]
	submit_time = submit_time.replace("\n", "")

	# Get current time
	start = datetime.strptime(submit_time, "%m.%d.%Y %H:%M:%S")
	now = datetime.now().strftime("%m.%d.%Y %H:%M:%S")
	end = datetime.strptime(now, "%m.%d.%Y %H:%M:%S")
	time_passed = end - start
	time_passed = str(time_passed)

	# If a week has passed since job submission, don't display live status
	if "days" in time_passed:
		num_days = int(time_passed.split(" ")[0])

		if num_days >= 7:
			expired = True

	# Look up table for ID and job suffix
	report_sum = dict()
	report_sum["PENDING"] = 0
	report_sum["RUNNING"] = 0
	report_sum["COMPLETED"] = 0
	report_sum["FAILED"] = 0
	report_sum["CANCELLED"] = 0

	# Display live status
	if not expired:
		print ""
		print " LIVE REPORT:"
		print " ------------------------------------------------------------------------------- "

		for ID, name in sorted(ID_LT.iteritems()):
			report = commands.getoutput("sacct --jobs=%s" % ID)

			for key in report_sum:
				if key in report:
					report_sum[key] += 1
					print " %s (%s): %s" % (key, ID, name)

		print ""
		for state, count in sorted(report_sum.iteritems()):
			print " %d%% %s" % (float(report_sum[state]*100.0/len(ID_LT)), state)
		print ""

	else:
		print " Live record disabled. Over a week has passed since job submission."
		print ""



	# STEP 2: ERROR CHECKER
	if report_sum["PENDING"] == 0 and report_sum["RUNNING"] == 0:
		print " ERROR REPORT:"
		print " ------------------------------------------------------------------------------- "

		ERR_LT = dict()
		for ID, name in sorted(ID_LT.iteritems()):
			error_name = name.replace(".sh", ".err")
			path = "%s/%s" % (ERR, error_name)

			if not os.path.isfile(path):
				print "%s does not exist. Job most likely failed." % error_name

			else:
				stat = int(commands.getoutput("stat -c%%s %s" % path))
				
				if stat not in ERR_LT:
					ERR_LT[stat] = [error_name]
				else:
					ERR_LT[stat].append(error_name)

		for stat, names in sorted(ERR_LT.iteritems()):
			print " %i bytes:" % stat

			for n in names:
				print " %s" % n

			print ""

		print " Sbatch outputs text into .err files, even if they are not error messages."
		print " Error files of uniform size can normally be trusted, while error files of differing"
		print " sizes should be viewed."
		print ""

		view = ""
		while view != "done":
			print " ------------------------------------------------------------------------------- "
			print " Input error file name as listed above to view its contents,"
			print " or type 'done' to return to the step 2 menu."
			print ""

			view = raw_input(" >>> ")

			if view != "done":

				path = "%s/%s" % (ERR, view)

				if not os.path.isfile(path):
					sys.exit(" ERROR: The name you inputted does not exist.")

				print " From path: %s" % path
				print " ------------------------------------------------------------------------------- "
				print ""
				print commands.getoutput("cat %s" % path)
				print ""

if __name__ == '__main__':
	main()


