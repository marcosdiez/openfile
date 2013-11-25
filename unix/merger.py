#!/usr/bin/env python
import of
import sys
import os.path
import os
import subprocess

winmerge="c:\progs\WinMerge-2.8.4-exe\WinMergeU.exe"

def check_parameters():
	if len(sys.argv) < 3:
		print "usage: {} FIRST_BRANCH SECOND_BRANCH FILE".format(sys.argv[0])
		sys.exit(0)

	the_file = sys.argv[3]
	if not os.path.isfile(the_file):
		print "File {} does not exist.".format(the_file)
		sys.exit(0)

def obtin_files(the_file, first_branch, second_branch):
	def run_cmd(the_parameters, target_file):
		print the_parameters
		subprocess.check_output(the_parameters)
		the_file = the_parameters[3]
		print "renaming [{}] to [{}]".format(the_file, target_file)
		os.rename(the_file, target_file)

	os.rename(the_file, the_file + ".tmp")

	mask = "/tmp/{}.{}.{}".format(the_file,"{}",of.get_file_extension(the_file))
	first_file = mask.format(first_branch.replace("/","_"))
	second_file = mask.format(second_branch.replace("/","_"))

	run_cmd(["git", "checkout", first_branch , the_file], first_file)
	#os.rename(the_file, first_file)

	run_cmd(["git", "checkout", second_branch , the_file], second_file)
	#os.rename(the_file, second_file)


	os.rename(the_file + ".tmp", the_file)

	return first_file , second_file

def main():
	check_parameters()
	the_file = sys.argv[3]
	first_branch = sys.argv[1]
	second_branch = sys.argv[2]
	first_file , second_file= obtin_files(the_file,first_branch,second_branch)

	first_path = of.convert_path(first_file)
	second_path = of.convert_path(second_file)

	the_command = "{} {} {}".format(winmerge, first_path, second_path)
	of.send_socket_cmd(the_command)


if __name__=="__main__":
#	import rpdb2; rpdb2.start_embedded_debugger("123")
	main()

