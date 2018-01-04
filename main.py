import os
import sys
import imp

# Import processing modules
readers = imp.load_source("readers", "./processing_scripts/readers.py")

def main():
	my_task = readers.default_reader("./tasks/test_task.txt")
	my_constructor = readers.default_reader("./constructors/test_constructor.txt")
	my_genome = readers.genome_reader("./genome_tables/%s" % my_task["REF TABLE"], my_task["REF ID"])

	for k in my_constructor:
		print "%s: %s" % (k, my_constructor[k])

if __name__ == '__main__':
	main()

