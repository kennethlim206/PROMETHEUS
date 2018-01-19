import os
import sys
import imp

# Import processing modules
readers = imp.load_source("readers", "./processing_scripts/readers.py")
interpreter = imp.load_source("interpreter", "./processing_scripts/interpreter.py")

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
	constructor_exit = 0
	
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
			sys.exit("Ending instance...")

		task_input_path = "./tasks/%s" % task_input

		# Error for non-existing user input
		if not os.path.isfile(task_input_path):
			sys.exit("ERROR: Inputted task name does not exist.")
		else:
			print "You selected the input file: %s\n" % task_input

		while not constructor_exit:

			# Input function from user
			print " ------------------------------------------------------------------------------- "
			print "|              STEP 2: PLEASE CHOOSE A FUNCTION TO PERFORM OR EXIT              |"
			print " ------------------------------------------------------------------------------- "

			# Display all functions from constructor table
			constructor_files = open("./function_constructors/chooseFunction_table.txt", "r")
			constructor_d = dict()
			for line in constructor_files:
				if "#" not in line:
					data = line.split("\t")
					name = data[0]
					input_name = data[1]
					description = data[2]

					print "%s = %s" % (input_name, description)

					constructor_d[input_name] = name

			constructor_files.close()

			print "exit"
			print " ------------------------------------------------------------------------------- "
			print ""

			constructor_input = raw_input(">>> ")

			if constructor_input == "exit":
				sys.exit("Ending instance...")

			# Error for non-existing user input
			if constructor_input not in constructor_d:
				sys.exit("ERROR: Inputted function name does not exist.")
			else:
				print "You selected the function: %s\n" % constructor_input

			constructor_input_path = "./function_constructors/%s" % constructor_d[constructor_input]



			####### Start stuff #######



			my_task = readers.task_reader(task_input_path)
			my_constructor = readers.constructor_reader(constructor_input_path)
			my_genome = readers.genome_reader("./genome_tables/%s" % my_task["REF TABLE"], my_task["REF ID"])

			interpreter.interpret(my_constructor, my_task, my_genome)



			####### End stuff #######



			print " ------------------------------------------------------------------------------- "
			print "Are there other functions you wish to run on this dataset: %s ? (Y/N)\n" % task_input
			more_constructor = raw_input(">>> ")

			if more_constructor == "N":
				constructor_exit = 1
			elif more_constructor == "Y":
				task_exit = 0
				constructor_exit = 0
			else:
				sys.exit("Incorrect input. Exiting program...")

		print " ------------------------------------------------------------------------------- "
		print "Would you like to choose a new dataset? (Y/N)\n"
		more_task = raw_input(">>> ")

		if more_task == "N":
			task_exit = 1
		elif more_task == "Y":
				task_exit = 0
				constructor_exit = 0
		else:
			sys.exit("Incorrect input. Exiting program...")

	print ""
	print "Bye for now!"

if __name__ == '__main__':
	main()

