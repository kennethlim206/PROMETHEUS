import os
import sys
import commands

def get_other(directory, suffix):
	status, sdout = commands.getstatusoutput("find %s -not -path '*/\.*' -type f -name '*%s*'" % (directory, suffix))
	if status == 0:
		return_list = sorted(sdout.split("\n"))

		if return_list[0] == "":
			sys.exit("ERROR: No files with the given suffix found in given directory: %s" % directory)
		else:
			return return_list
	else:
		sys.exit("ERROR: %s" % sdout)

def get_FASTQs(directory):
	status, sdout = commands.getstatusoutput("find %s -not -path '*/\.*' -type f -name '*.fastq*'" % directory)
	if status == 0:
		return_list = sorted(sdout.split("\n"))

		if return_list[0] == "":
			sys.exit("ERROR: No fastq files found in the given directory: %s" % directory)
		else:
			return return_list
	else:
		sys.exit("ERROR: %s" % sdout)

def get_BAMs(directory):
	status, sdout = commands.getstatusoutput("find %s -not -path '*/\.*' -type f -name '*.sortedByCoord.out.bam'" % directory)
	if status == 0:
		sorted_list = sorted(sdout.split("\n"))
		return_list = []

		for i in sorted_list:
			if ".bai" not in i:
				return_list.append(i)

		if return_list[0] == "":
			sys.exit("ERROR: No bam files found in given directory: %s" % directory)
		else:
			return return_list
	else:
		sys.exit("ERROR: %s" % sdout)

def populate(directory, task, function):

	make_d = dict()
	make_d["root directory"] = directory.rsplit("/", 1)[0]
	make_d["directory"] = directory
	make_d["red"] = "%s/RED" % directory
	make_d["output"] = "%s/sbatch_output" % make_d["red"]
	make_d["error"] = "%s/sbatch_error" % make_d["red"]
	make_d["scripts"] = "%s/sbatch_scripts" % make_d["red"]
	make_d["user"] = "%s/user_input" % make_d["red"]

	if not os.path.isdir(make_d["root directory"]):
			os.popen("mkdir %s" % make_d["root directory"])
	if not os.path.isdir(make_d["directory"]):
			os.popen("mkdir %s" % make_d["directory"])
	if not os.path.isdir(make_d["red"]):
			os.popen("mkdir %s" % make_d["red"])
			
	for key in make_d:
		if not os.path.isdir(make_d[key]):
			os.popen("mkdir %s" % make_d[key])

	os.popen("cp -r %s %s" % (task, make_d["user"]))
	os.popen("cp -r %s %s" % (function, make_d["user"]))
	# os.popen("cp -r ./processing_scripts/find.py %s" % make_d["red"])

	return make_d