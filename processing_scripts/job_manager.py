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



	# JASK: GET AUTO DEPENDENT SCRIPTS HERE

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

	print " ------------------------------------------------------------------------------- "
	print "Constructing your requests..."
	print ""
	
	# Interpret functions
	dependency = ""
	for my_function in function_queue:
		dependency = interpreter.interpret(my_task, my_genome, my_function, dependency)
		print dependency



	

	

	