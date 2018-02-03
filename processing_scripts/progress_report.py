import os
import sys
import imp
import datetime
import commands

def main(t,f):

	# Import processing modules
	tools = imp.load_source("tools", "./processing_scripts/burst_tools.py")

	# Load task info from reader
	td = tools.task_reader(t)


	if f == ""



	

if __name__ == '__main__':
	main()