import os
import sys
import commands

def interpret(cd, td):

	# Figuring out dependency. Manual = get dependency ID from user.
	DEPENDENCY_ID = ""
	if cd["DEPENDENCY"] == "MANUAL":
		print "Is the job you selected dependent upon a previous job? (Y/N)\n"
		answer = raw_input(">>> ")

		if answer == "Y":
			print "You entered Yes. Input job ID that the selected jobs will be dependent upon.\n"
			DEPENDENCY_ID = raw_input(">>> ")
			
		elif answer == "N":
			print "You entered No. Selected jobs will run independent of any previous jobs."
		else:
			sys.exit("ERROR: incorrect input to dependency query.")

	# Figuring out dependency. Auto:[JOB NAME] = automatically creates dependency from function constructor.
	elif "AUTO:" in cd["DEPNDENCY"]:
		print "Justin: I will build auto-dependency later, 01/09."

	else:
		sys.exit("ERROR: incorrect input to <DEPENDENCY> cmd in function constructor sheet.")

	# Convert INPUT DIR to directory containing input files
	if cd["INPUT DIR"] == "URL":
		print "Justin: I will build URL input later, 01/09."

	elif cd["INPUT DIR"] == "RAW":
		print "Justin: I will build RAW input later, 01/09."

	elif cd["INPUT DIR"] == "INDEX":
		print "Justin: I will build INDEX input later, 01/09."

	elif "POST:" in cd["INPUT DIR"]:

		# Find correct input directory 
		POST_NAME = cd["INPUT DIR"].split("POST:")[1]
		INPUT_DIR = "%s/%s" % (td["POST DIR"], POST_NAME)

		if not os.path.isdir(INPUT_DIR):
			sys.exit("ERROR: <INPUT DIR> in function constructor does not exist.")
	else:
		sys.exit("ERROR: Incorrect input into <INPUT DIR> command in function constructor.")

	# Generate script
	cmd = cd["SCRIPT COMMAND"]
	for var in td:
		if "<%s>" % var in cmd:
			cmd = cmd.replace("<%s>" % var, td[var])

	print cmd





