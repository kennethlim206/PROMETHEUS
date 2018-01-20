import os
import sys
import commands
import imp

tools = imp.load_source("tools", "./processing_scripts/interpreter_tools.py")

def interpret(cd, td, gd):

	######################
	###   DEPENDENCY   ###
	######################

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
	elif "AUTO:" in cd["DEPENDENCY"]:
		print "Justin: I will build auto-dependency later, 01/09."

	else:
		sys.exit("ERROR: incorrect input to <DEPENDENCY> cmd in function constructor sheet.")



	#####################
	###   INPUT DIR   ###
	#####################

	# INPUT PART 1: Convert INPUT DIR to directory containing input files
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
		cd["INPUT DIR"] = INPUT_DIR

		if not os.path.isdir(INPUT_DIR):
			sys.exit("ERROR: <INPUT DIR> in function constructor does not exist.")
	else:
		sys.exit("ERROR: Incorrect input into <INPUT DIR> command in function constructor.")

	# INPUT PART 2: Retrieve INPUT DIR files based on suffix
	if cd["INPUT SUFFIX"] == "FASTQ":
		cd["INPUT FILES FULL"] = tools.get_FASTQs(cd["INPUT DIR"])
	elif cd["INPUT SUFFIX"] == "BAM":
		cd["INPUT FILES FULL"] = tools.get_BAMs(cd["INPUT DIR"])
	elif "POST:" in cd["INPUT SUFFIX"]:
		SUFFIX = cd["INPUT SUFFIX"]
		SUFFIX = SUFFIX.split(":")[1]
		cd["INPUT FILES FULL"] = tools.get_other(cd["INPUT DIR"], SUFFIX)
	else:
		sys.exit("ERROR: Incorrect input into <INPUT SUFFIX> command in function constructor.")

	# INPUT PART 3: Trim INPUT FILES to get rid of prefix paths
	cd["INPUT FILES TRIMMED"] = []
	for file in cd["INPUT FILES FULL"]:
		split_file = file.split("/")
		trimmed_file = split_file[len(split_file)-1]
		cd["INPUT FILES TRIMMED"].append(trimmed_file)



	######################
	###   OUTPUT DIR   ###
	######################

	# OUTPUT PART 1: Convert OUTPUT DIR type to real directory
	if cd["OUTPUT DIR"] == "RAW":
		cd["OUTPUT DIR"] = td["RAW DATA DIR"]
	elif cd["OUTPUT DIR"] == "INDEX":
		cd["OUTPUT DIR"] = td["INDEX DIR"]
	elif "POST:" in cd["OUTPUT DIR"]:
		NAME = cd["OUTPUT DIR"].split(":")[1]
		cd["OUTPUT DIR"] = "%s/%s" % (td["POST DIR"], NAME)
	else:
		sys.exit("ERROR: Incorrect input into <OUTPUT> command in function constructor.")

	# OUTPUT PART 2: Create and populate OUTPUT DIR
	record = tools.populate(cd["OUTPUT DIR"], td["PATH"], cd["PATH"])



	###########################
	###   REF FA AND ANNO   ###
	###########################

	# Decide whether to use customized ref genome and annotation
	if td["CUSTOMIZE"] == "T":
		td["USE FA"] = "%s/custom_genome/%s" % (td["INDEX DIR"], td["CUSTOM FA"])
		td["USE ANNO"] = "%s/custom_genome/%s" % (td["INDEX DIR"], td["CUSTOM ANNO"])
	elif td["CUSTOMIZE"] == "F":
		td["USE FA"] = gd["REF FA"]
		td["USE ANNO"] = gd["CUSTOM ANNO"]



	############################
	###   GENERATE SCRIPTS   ###
	############################

	# Add task variables to script
	cmd = cd["SCRIPT COMMAND"]
	for var in td:
		if "<%s>" % var in cmd:
			cmd = cmd.replace("<%s>" % var, td[var])

	# Add function variables to script
	safe_list = ["INPUT FILES FULL", "INPUT FILES TRIMMED"]
	for var in cd:
		if var not in safe_list:
			if "<%s>" % var in cmd:
				cmd = cmd.replace("<%s>" % var, cd[var])

	# Write script
	for i in range(0, len(cd["INPUT FILES FULL"])):
		cmd_ind = cmd
		input_full_ind = cd["INPUT FILES FULL"][i]
		input_trim_ind = cd["INPUT FILES TRIMMED"][i]

		cmd_ind = cmd_ind.replace("<INPUT FILES FULL>", input_full_ind)
		cmd_ind = cmd_ind.replace("<INPUT FILES TRIMMED>", input_trim_ind)

		# Place in RED of OUTPUT DIR
		script_ind = open("%s/%s.sh" % (record["scripts"], input_trim_ind), "w")

		script_ind.write("#!/bin/bash -l\n\n")

		# Required for sbatch script
		script_ind.write("#SBATCH --job-name=%s\n" % cd["FUNCTION NAME"])
		script_ind.write("#SBATCH --time=%s\n" % cd["TIME"])
		script_ind.write("#SBATCH --output=%s/%s,out\n" % (record["output"], input_trim_ind))
		script_ind.write("#SBATCH --error=%s/%s.err\n" % (record["error"], input_trim_ind))

		# Optional for sbatch script
		if cd["PARTITION"] != "default":
			script_ind.write("#SBATCH --partition=%s\n" % cd["PARTITION"])

		if cd["CORES"] != "default":
			script_ind.write("#SBATCH --cores=%s\n" % cd["CORES"])

		if cd["MEM PER CPU"] != "default":
			script_ind.write("#SBATCH --mem-per-cpu=%s\n" % cd["MEM PER CPU"])

		script_ind.write("")
		script_ind.write(cmd_ind)
		script_ind.write("")

		script_ind.close()



		




	

	

	





