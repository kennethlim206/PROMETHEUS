import os
import sys
import imp
import commands
import time

# Figures out the order for function requests
def main():
	task_path = sys.argv[1]
	function_string = sys.argv[2]

	print " ------------------------------------------------------------------------------- "
	print " Submitting your BURST modules: "
	print ""

	function_list = function_string.split("+")

	
	# Interpret functions
	submitter_dependency = ""
	ID_num = 1738
	
	for i in range(0,len(function_list)):
		function_path = function_list[i]
		cmd = "srun"

		if i > 0:
			# Grab dependency from previous submission
			cmd += " --dependency=afterok:%s" % submitter_dependency

		cmd += " --time=00:15:00 ./processing_scripts/burst_submitter.sh %s %s" % (task_path, function_path)

		print " Submitting function %i/%i - %s" % (i+1, len(function_list), function_path.rsplit("/", 1)[1])
		print " %s" % cmd
		status = 0
		ID = "%i:%i" % (ID_num, ID_num+1)
		ID_num += 2

		# Non test case
		if len(sys.argv) == 3:
			status, ID = commands.getstatusoutput(cmd)

		# Read sbatch output
		if status == 0:
			print ID
			print ""
			submitter_dependency = str(ID)
		else:
			sys.exit(" ERROR:\n%s" % ID)

		time.sleep(60)

if __name__ == '__main__':
	main()

