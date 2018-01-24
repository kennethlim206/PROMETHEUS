import os
import sys
import imp

# Import processing modules
manager = imp.load_source("manager", "./processing_scripts/job_manager.py")

# User interface
def main():

	print "\n"
	print "*********************************************************************************  "
	print "*                        __       __         __                                 *  "
	print "*   ________________    |  |  |  |  |  |    |    |   |    ________________|\\    * "
	print "*  |                    |__|  |  |__|  |    |__  |___|                      \\   * "
	print "*  |________________    |\\    |  |     |    |      |      ________________  /   * "
	print "*                       | \\   |  |     |__  |__    |                      |/    * "
	print "*                                                                               *  "
	print "*********************************************************************************  "
	print "         - THE NORDLAB RNA-SEQ INTERACTIVE PIPELINE EXPERIMENT YIELDER -           "
	print "\n"

	# Keeps user in the interface, until they choose to exit
	task_exit = 0
	function_exit = 0
	
	while not task_exit:

		# Input task from user
		print " ------------------------------------------------------------------------------- "
		print "|           STEP 1: PLEASE CHOOSE THE NAME OF YOUR TASK FILE OR EXIT            |"
		print " ------------------------------------------------------------------------------- "

		# Display all task options
		input_files = os.listdir("./tasks")
		input_files.sort()
		for file in input_files:
			print file

		print ""
		print "exit"
		print " ------------------------------------------------------------------------------- "
		print ""

		task_input = raw_input(">>> ")

		if task_input == "exit":
			sys.exit("Bye for now!")

		task_input_path = "./tasks/%s" % task_input

		# Error for non-existing user input
		if not os.path.isfile(task_input_path):
			sys.exit("ERROR: Inputted task name does not exist.")
		else:
			print "You selected the input file: %s\n" % task_input

		while not function_exit:

			# Input function from user
			print " ------------------------------------------------------------------------------- "
			print "|                  STEP 2: PLEASE CHOOSE A FUNCTION(S) OR EXIT                  |"
			print " ------------------------------------------------------------------------------- "
			print " Note: Users can perform functions sequentially with the '->' symbol."
			print " Example: download->align->feature"
			print ""

			# Display all functions from function table
			function_files = open("./function_constructors/chooseFunction_table.txt", "r")
			function_d = dict()
			for line in function_files:
				if "#" not in line:
					line = line.replace("\n", "")
					data = line.split("\t")
					name = data[0]
					input_name = data[1]
					description = data[2]

					print "%s = %s" % (input_name, description)

					function_d[input_name] = name

			function_files.close()

			print ""
			print "exit"
			print " ------------------------------------------------------------------------------- "
			print ""

			function_input = raw_input(">>> ")

			if function_input == "exit":
				sys.exit("Bye for now!")



			# Import relevant information to job manager
			manager.run(task_input_path, function_input, function_d)



			# Ask to repeat
			print " ------------------------------------------------------------------------------- "
			print "Are there other functions you wish to run on this dataset: %s ? (Y/N/exit)\n" % task_input
			more_function = raw_input(">>> ")

			if more_function == "N":
				function_exit = 1
			elif more_function == "Y":
				task_exit = 0
				function_exit = 0
			elif more_function == "exit":
				sys.exit("Bye for now!")
			else:
				sys.exit("Incorrect input. Exiting program...")

		print " ------------------------------------------------------------------------------- "
		print "Would you like to choose a new dataset? (Y/N/exit)\n"
		more_task = raw_input(">>> ")

		if more_task == "N":
			task_exit = 1
		elif more_task == "Y":
			task_exit = 0
			function_exit = 0
		elif more_task == "exit":
			sys.exit("Bye for now!")
		else:
			sys.exit("Incorrect input. Exiting program...")

	print "Bye for now!"

if __name__ == '__main__':
	main()

