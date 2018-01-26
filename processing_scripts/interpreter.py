import os
import sys
import commands
import imp

def main():

	# Import processing modules
	readers = imp.load_source("readers", "./processing_scripts/readers.py")
	tools = imp.load_source("tools", "./processing_scripts/interpreter_tools.py")

	# Load task info from reader
	td = readers.task_reader(sys.argv[1])
	cd = readers.function_reader(sys.argv[2])
	gd = readers.genome_reader("./genome_tables/%s" % td["REF TABLE"], td["REF ID"])



	#####################
	###   INPUT DIR   ###
	#####################

	# INPUT PART 1: Convert INPUT DIR to directory containing input files
	if cd["INPUT DIR"] == "URL":
		cd["INPUT DIR"] = td["FTP COMMAND"]

	elif cd["INPUT DIR"] == "RAW":
		cd["INPUT DIR"] = td["RAW DATA DIR"]

	elif cd["INPUT DIR"] == "INDEX":
		cd["INPUT DIR"] = td["INDEX DIR"]

	elif "POST:" in cd["INPUT DIR"]:

		# Find correct input directory 
		POST_NAME = cd["INPUT DIR"].split("POST:")[1]
		INPUT_DIR = "%s/%s" % (td["POST DIR"], POST_NAME)
		cd["INPUT DIR"] = INPUT_DIR

	else:
		sys.exit("ERROR: Incorrect input into <INPUT DIR> command in function constructor.")

	# If INPUT DIR is a URL, then the command does not require further parsing.
	if cd["INPUT DIR"] != "URL":

		# Check if input directory is actual directory
		if not os.path.isdir(cd["INPUT DIR"]):
			sys.exit("ERROR: task sheet variable associated with <INPUT DIR> does not exist: %s" % cd["INPUT DIR"])

		# INPUT PART 2: Retrieve INPUT DIR files based on suffix
		if cd["INPUT SUFFIX"] == "FASTQ":
			cd["INPUT FILES FULL"] = tools.get_FASTQs(cd["INPUT DIR"])

		elif cd["INPUT SUFFIX"] == "BAM":
			cd["INPUT FILES FULL"] = tools.get_BAMs(cd["INPUT DIR"])

		elif "POST:" in cd["INPUT SUFFIX"]:
			SUFFIX = cd["INPUT SUFFIX"]
			SUFFIX = SUFFIX.split(":")[1]
			cd["INPUT FILES FULL"] = tools.get_other(cd["INPUT DIR"], SUFFIX)

		elif cd["INPUT SUFFIX"] == "NONE":
			cd["INPUT FILES FULL"] = [cd["FUNCTION NAME"]]

		else:
			sys.exit("ERROR: Incorrect input into <INPUT SUFFIX> command in function constructor.")

		# INPUT PART 3: Trim INPUT FILES to get rid of prefix paths
		cd["INPUT FILES TRIMMED"] = []
		for file in cd["INPUT FILES FULL"]:
			trimmed_file = file.rsplit("/", 1)[1]
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



	####################################
	###   ALIGNING PAIRED-END DATA   ###
	####################################

	if cd["FUNCTION NAME"] == "ALIGN":
		for i in range(0,len(cd["INPUT FILES TRIMMED"])):
			if td["SINGLE PAIR"] == "SE":
				cd["INPUT FILES TRIMMED"][i] = cd["INPUT FILES TRIMMED"][i].replace(td["FASTQ SUFFIX"], "_SE")

			elif td["SINGLE PAIR"] == "PE":
				cd["INPUT FILES TRIMMED"][i] = cd["INPUT FILES TRIMMED"][i].replace(td["FASTQ SUFFIX"], "_PE")

			else:
				sys.exit("ERROR: Incorrect input into <PAIRED SUFFIX> task variable.")



	#######################
	###   ZIPPED DATA   ###
	#######################

	if td["ZIPPED"] == ".gz":
		td["ZIPPED"] = "--readFilesCommand gunzip -c"
	elif td["ZIPPED"] == ".bzip2":
		td["ZIPPED"] = "--readFilesCommand bunzip2 -c"
	elif td["ZIPPED"] == "":
		td["ZIPPED"] = ""
	else:
		sys.exit("ERROR: Incorrect input into <ZIPPED> task variable.")



	############################
	###   GENERATE SCRIPTS   ###
	############################

	test_num = 1738

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

	# Write and run script
	return_string = ""

	for i in range(0, len(cd["INPUT FILES FULL"])):
		cmd_ind = cmd
		input_full_ind = cd["INPUT FILES FULL"][i]
		input_trim_ind = cd["INPUT FILES TRIMMED"][i]

		cmd_ind = cmd_ind.replace("<INPUT FILES FULL>", input_full_ind)
		cmd_ind = cmd_ind.replace("<INPUT FILES TRIMMED>", input_trim_ind)

		script_ind_path = "%s/%s.sh" % (record["scripts"], input_trim_ind)

		# Place in RED of OUTPUT DIR
		script_ind = open(script_ind_path, "w")

		script_ind.write("#!/bin/bash -l\n\n")

		# Required for sbatch script
		script_ind.write("#SBATCH --job-name=%s\n" % cd["FUNCTION NAME"])
		script_ind.write("#SBATCH --time=%s\n" % cd["TIME"])
		script_ind.write("#SBATCH --output=%s/%s.out\n" % (record["output"], input_trim_ind))
		script_ind.write("#SBATCH --error=%s/%s.err\n" % (record["error"], input_trim_ind))

		# Optional for sbatch script
		if cd["PARTITION"] != "default":
			script_ind.write("#SBATCH --partition=%s\n" % cd["PARTITION"])

		if cd["CORES"] != "default":
			script_ind.write("#SBATCH --cpus-per-task=%s\n" % cd["CORES"])

		if cd["MEM PER CPU"] != "default":
			script_ind.write("#SBATCH --mem-per-cpu=%s\n" % cd["MEM PER CPU"])



		script_ind.write("")
		script_ind.write(cmd_ind)
		script_ind.write("")

		script_ind.close()




		#########################
		###   SUBMIT SCRIPT   ###
		#########################

		submission_record = open("%s/submission_record.txt" % record["red"], "a")

		print "Submitting job %s: %i/%i" % (cd["FUNCTION NAME"], i+1, len(cd["INPUT FILES FULL"]))

		submit_cmd = "sbatch %s" % script_ind_path
		
		status = 0
		ID = "Submitting job as %i" % test_num
		test_num += 1

		if len(sys.argv) == 3:
			status, ID = commands.getstatusoutput(submit_cmd)

		# Analyze result of sbatch submission
		if status == 0:

			ID_split = ID.split(" ")
			ID = int(ID_split[3])

			return_message = "Job %s submitted as %i" % (cd["FUNCTION NAME"], ID)

			print return_message
			
		else:
			sys.exit("ERROR: Sbatch submission error: %s" % ID)

		submission_record.write("%s\n" % submit_cmd)
		submission_record.write("%s\n" % return_message)
		return_string += "%s:" % ID

	submission_record.write("\n")
	submission_record.close()
	
	temp_dep = open("./processing_scripts/temp/dependency.txt", "w")
	temp_dep.write("<DEPENDENCY> %s" % return_string[:len(return_string)-1])
	temp_dep.close()

if __name__ == '__main__':
	main()
