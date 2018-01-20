import os
import sys
import commands

def main():

	print "-------------------------------------------------------------------"
	print "You may search for the following:\n"
	print "1. Date (MM.DD.YYYY)"
	print "2. Sbatch Job ID"
	print "3. String in inputted command (slurm output file, slurm error file, etc.)\n"
	print "-------------------------------------------------------------------\n"

	ID = raw_input("Search: ")
	print""

	status, sdout = commands.getstatusoutput("grep -n '%s' slurm_record.txt" % ID)

	if status == 0:
		add = 0
		if "Sumbitted on:" in sdout and "Job ID Number:" not in sdout and "Submitted with command:" not in sdout:
			print "Date input detected. Here are all the entries for your chosen date:"
			print "-------------------------------------------------------------------\n"
			add = 2

		elif "Job ID Number:" in sdout and "Sumbitted on:" not in sdout:
			print "Job ID input detected. Here are all the entries for your chosen ID:"
			print "-------------------------------------------------------------------\n"
			add = 1

		elif "Submitted with command:" in sdout and "Sumbitted on:" not in sdout:
			print "Input string detected. Here are all the entries for your chosen string:"
			print "-------------------------------------------------------------------\n"
		else:
			sys.exit("ERROR: Input too general. Please input more specific string.")

		# If multiple entries are found, split and iterate through all of them
		data = sdout.split("\n")

		print "        ||        "
		print "        ||        "
		print "        ||        "
		print "       _||_       "
		print "      \    /      "
		print "       \  /       "
		print "        \/        "
		print""

		for line in data:
			num = line.split(":")[0]

			num = int(num) + add
			status, sdout = commands.getstatusoutput("sed '%iq;d' slurm_record.txt" % num)
			print "-------------------------------------------------------------------"
			if sdout != "":
				if add > 0:
					print line.split(":", 1)[1]
				print sdout
				data = sdout.split(" ")
				for var in data:
					if "--output=" in var:
						var = var.replace("--output=","")
						print "-------------"
						print "SLURM OUTPUT:"
						print "From path: %s" % var
						status, sdout = commands.getstatusoutput("cat %s" % var)
						print sdout
					if "--error=" in var:
						var = var.replace("--error=","")
						print "-------------"
						print "SLURM ERROR:"
						print "From path: %s" % var
						status, sdout = commands.getstatusoutput("cat %s" % var)
						print sdout
						print "-------------------------------------------------------------------\n"

		print "All done! :)"

	else:
		sys.exit("ERROR: String not found. Please select different string.")

if __name__ == '__main__':
	main()