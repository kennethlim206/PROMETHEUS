import os
import sys

def _get_SRAs(self, DIR):
	status, sdout = commands.getstatusoutput("find %s -not -path '*/\.*' -type f -name '*.sra'" % DIR)
	if status == 0:
		return_list = sorted(sdout.split("\n"))

		if return_list[0] == "":
			sys.exit("ERROR: no sample files found in given directory: %s" % DIR)
		else:
			return return_list

	else:
		sys.exit("ERROR: %s" % sdout)

def _get_FQs(self, DIR):
	status, sdout = commands.getstatusoutput("find %s -not -path '*/\.*' -type f -name '*%s*'" % (DIR, self.d["FASTA SUFFIX"]))
	if status == 0:
		return_list = sorted(sdout.split("\n"))

		if return_list[0] == "":
			sys.exit("ERROR: no sample files found in given directory: %s" % DIR)
		else:
			return return_list

	else:
		sys.exit("ERROR: %s" % sdout)

def _get_BAMs(self, DIR):
	status, sdout = commands.getstatusoutput("find %s -not -path '*/\.*' -type f -name '*.sortedByCoord.out.bam'" % DIR)
	if status == 0:
		sorted_list = sorted(sdout.split("\n"))
		return_list = []

		for i in sorted_list:
			if ".bai" not in i:
				return_list.append(i)

		if return_list[0] == "":
			sys.exit("ERROR: no sample files found in given directory: %s" % DIR)
		else:
			return return_list

	else:
		sys.exit("ERROR: %s" % sdout)

def _populate(self, DIR):

	red = "%s/RED" % DIR
	red_o = "%s/slurm_output" % red
	red_e = "%s/slurm_error" % red

	if not os.path.isdir(DIR):
		os.popen("mkdir %s" % DIR)
	if not os.path.isdir(red):
		os.popen("mkdir %s" % red)
	if not os.path.isdir(red_o):
		os.popen("mkdir %s" % red_o)
	if not os.path.isdir(red_e):
		os.popen("mkdir %s" % red_e)

	os.popen("cp -r %s %s" % (self.d["INPUT VARS"], red))
	os.popen("cp -r %s/find.py %s" % (self.d["PROCESSING DIR"], red))

	return [red, red_o, red_e]