import os
import sys
import imp
import commands
import time

# Figures out the order for function requests
def run(task_path, function_path_list):

	# Get auto call functions in order as well
	all_function_list = []
	for path in function_path_list:
		all_function_list.append(path)

		auto_call = commands.getoutput("grep '<AUTO CALL>' %s" % path)
		auto_call = auto_call.split("<AUTO CALL>")[1]
		auto_call = auto_call.replace(" ", "")
		auto_call = auto_call.replace("\n", "")

		if auto_call != "":
			auto_path = "./function_constructors/%s" % auto_call

			# Error for non-existing autocall input
			if not os.path.isfile(auto_path):
				sys.exit(" ERROR: Incorrect <AUTO CALL> file name. Please check function constructor: %s" % path.rsplit("/", 1)[1])

			all_function_list.append(auto_path)

		

	print " ------------------------------------------------------------------------------- "
	print " Constructing your request ..."
	print ""
	
	# Interpret functions
	for i in range(0,len(all_function_list)):

		cmd = "sbatch "

		# Grab dependency numbers from submitter output
		if i > 0:
			dependency = commands.getoutput("grep '<DEPENDENCY>' ./processing_scripts/temp/submitter.out")
			dependency = dependency.replace("<DEPENDENCY> ", "")
			dependency = dependency.replace("\n", "")

			cmd += dependency

		cmd += " %s %s" % (task_path, all_function_list[i])

		# Feed job dependency through
		# Make this section dependent submitters




		



	

	

	