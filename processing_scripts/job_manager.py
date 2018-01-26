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

			print " + AUTO CALLED: %s" % auto_call

		

	print " ------------------------------------------------------------------------------- "
	print " Constructing your request ..."
	print ""
	
	# Interpret functions
	submitter_dependency = ""
	for i in range(0,len(all_function_list)):
		cmd = "srun --time=00:01:00"

		# if i > 0:
			# Grab dependency from previous submission
			# cmd += " --dependency=afterok:%s" % submitter_dependency

		cmd += " ./processing_scripts/root_submitter.sh %s %s" % (task_path, all_function_list[i])

		print " Submitting function %i/%i - %s" % (i+1, len(all_function_list), all_function_list[i].rsplit("/", 1)[1])
		print " %s" % cmd
		status, ID = commands.getstatusoutput(cmd)
		time.sleep(10)
		if status == 0:
			print "++++++"
			print ID
			print "++++++"
			ID = ID.rsplit("\n", 1)[1]
			ID_split = ID.split(" ")
			ID = int(ID_split[3])
			print " Function submitted as %i" % (ID)
		else:
			sys.exit(" ERROR: sbatch error:\n%s" % ID)

		submitter_dependency = str(ID)

