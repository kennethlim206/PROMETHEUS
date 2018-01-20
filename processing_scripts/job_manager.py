import os
import sys
import imp

# Import processing modules
readers = imp.load_source("readers", "./processing_scripts/readers.py")
interpreter = imp.load_source("interpreter", "./processing_scripts/interpreter.py")

# Figures out the order for function requests
def run(task_path, functions, function_options):

	# Load task info from reader (error checks are in main.py)
	my_task = readers.task_reader(task_path)
	my_genome = readers.genome_reader("./genome_tables/%s" % my_task["REF TABLE"], my_task["REF ID"])



	# Parse and load function info
	my_functions = []
	function_list = functions.split("->")

	print "You selected the following function(s):"

	for f in function_list:
		# Error for non-existing user input
		if f not in function_options:
			sys.exit("ERROR: Inputted function name does not exist: %s" % f)

		function_input_path = "./function_constructors/%s" % function_options[f]

		# Error for non-existing user input
		if not os.path.isfile(function_input_path):
			sys.exit("ERROR: Incorrect function path. Please check the input path in chooseFunction_table.txt")

		my_f = readers.function_reader(function_input_path)
		my_functions.append(my_f)

		print f

	

	

	