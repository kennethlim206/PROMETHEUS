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
	task_exit = False
	function_exit = False
	
	while not task_exit:

		# Input task from user
		print " ------------------------------------------------------------------------------- "
		print "|            STEP 1: PLEASE CHOOSE THE ID OF YOUR TASK FILE OR EXIT             |"
		print " ------------------------------------------------------------------------------- "

		# Display all task options
		input_files = os.listdir("./tasks")
		input_list = []
		for file in input_files:
			if file[0] != ".":
				input_list.append(file)
				
		input_list.sort()
		print " ID   Task Sheet"
		print " ----------------"
		for i in range(0, len(input_list)):
			print " %i = %s" % (i, input_list[i])

		print ""
		print " exit"
		print " ------------------------------------------------------------------------------- "
		print ""

		task_input = raw_input(" >>> ")

		if task_input == "exit":
			sys.exit(" Bye for now!")

		# Error for non-numeric input
		try:
			int(task_input)
		except ValueError:
			sys.exit(" ERROR: Input is not ID Number.")

		task_input = int(task_input)

		# Error for numeric input not in range
		if task_input >= len(input_list):
			sys.exit(" ERROR: Input is not listed.")

		task_input_path = "./tasks/%s" % input_list[task_input]

		# Error for non-existing user input
		if not os.path.isfile(task_input_path):
			sys.exit(" ERROR: Inputted task name does not exist.")
		else:
			print " You selected the input file: %s\n" % input_list[task_input]

		while not function_exit:

			# Input function from user
			print " ------------------------------------------------------------------------------- "
			print "|                  STEP 2: PLEASE CHOOSE A FUNCTION(S) OR EXIT                  |"
			print " ------------------------------------------------------------------------------- "
			print " Note: Users can perform functions sequentially with the '->' symbol."
			print " Example: download -> align -> feature"
			print ""

			# Display all functions from function table
			function_files = open("./function_constructors/paths.txt", "r")
			function_options = dict()
			for line in function_files:
				if "#" not in line:
					line = line.replace("\n", "")
					data = line.split("\t")
					name = data[0]
					input_name = data[1]
					description = data[2]

					print " %s = %s" % (input_name, description)

					function_options[input_name] = name

			function_files.close()

			print ""
			print " exit"
			print " ------------------------------------------------------------------------------- "
			print ""

			function_input = raw_input(" >>> ")

			if function_input == "exit":
				sys.exit(" Bye for now!")

			# Parse and load function info
			function_input = function_input.replace(" ",  "")
			function_names_list = function_input.split("->")

			function_path_list = []

			print " You have chosen the following function(s):"

			for name in function_names_list:

				# Error for non-existing user input
				if name not in function_options:
					sys.exit(" ERROR: Inputted function name does not exist: %s" % name)

				function_input_path = "./function_constructors/%s" % function_options[name]

				# Error for non-existing user input
				if not os.path.isfile(function_input_path):
					sys.exit(" ERROR: Incorrect function path. Please check the input path in ./function_constructors/paths.txt")

				function_path_list.append(function_input_path)

				print " %s" % name

			# Import relevant information to job manager
			file = open("./processing_scripts/temp/dependency.txt", "w")
			file.close()
			manager.run(task_input_path, function_path_list)



			# Ask to repeat
			print " ------------------------------------------------------------------------------- "
			print " Are there other functions you wish to run on your chosen dataset: %s ? (Y/N/exit)\n" % input_list[task_input]
			more_function = raw_input(" >>> ")

			if more_function == "N":
				function_exit = True
			elif more_function == "Y":
				task_exit = False
				function_exit = False
			elif more_function == "exit":
				sys.exit(" Bye for now!")
			else:
				sys.exit(" Incorrect input. Exiting program...")

		print " ------------------------------------------------------------------------------- "
		print " Would you like to choose a new dataset? (Y/N/exit)\n"
		more_task = raw_input(" >>> ")

		if more_task == "N":
			task_exit = True
		elif more_task == "Y":
			task_exit = False
			function_exit = False
		elif more_task == "exit":
			sys.exit(" Bye for now!")
		else:
			sys.exit(" Incorrect input. Exiting program...")

	print " Bye for now!"

if __name__ == '__main__':
	main()

