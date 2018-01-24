import os
import sys
import imp

# Import processing modules
readers = imp.load_source("readers", "./processing_scripts/readers.py")
interpreter = imp.load_source("interpreter", "./processing_scripts/interpreter.py")

# Figures out the order for function requests
def run(task_path, function_names, function_options):

	# Load task info from reader (error checks are in main.py)
	my_task = readers.task_reader(task_path)
	my_genome = readers.genome_reader("./genome_tables/%s" % my_task["REF TABLE"], my_task["REF ID"])



	# Parse and load function info
	function_queue = []
	function_names_list = function_names.split("->")

	print "You selected the following function(s):"

	for name in function_names_list:
		# Error for non-existing user input
		if name not in function_options:
			sys.exit("ERROR: Inputted function name does not exist: %s" % name)

		function_input_path = "./function_constructors/%s" % function_options[name]

		# Error for non-existing user input
		if not os.path.isfile(function_input_path):
			sys.exit("ERROR: Incorrect function path. Please check the input path in chooseFunction_table.txt")

		print name

		my_function = readers.function_reader(function_input_path)
		function_queue.append(my_function)

		# ADD AUTO CALLS
		if my_function["AUTO CALL"] != "":

			function_input_path = "./function_constructors/%s" % my_function["AUTO CALL"]

			# Error for non-existing user input
			if not os.path.isfile(function_input_path):
				sys.exit("ERROR: Incorrect input into <AUTO CALL> variable in function constructor.")

			print "AUTO CALLED: %s" % my_function["AUTO CALL"]

			called_function = readers.function_reader(function_input_path)
			function_queue.append(called_function)

		

	print " ------------------------------------------------------------------------------- "
	print "Constructing your request ..."
	print ""
	
	# Interpret functions
	dependency = ""
	for my_function in function_queue:

		# Dictionaries are mutable in python so passing an instance into a function will alter the original.
		# Making a copy of the original and altering the copy solves this problem.
		my_task_copy = dict(my_task)
		my_genome_copy = dict(my_genome)
		my_function_copy = dict(my_function)

		dependency = interpreter.interpret(my_task_copy, my_genome_copy, my_function_copy, dependency)



	

	

	