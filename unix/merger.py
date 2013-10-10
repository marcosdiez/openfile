#!/usr/bin/env python
"spawns winmerge from a file in two different git branches"
import of
import sys
import os.path
import os
import subprocess

WINMERGE = "c:\\progs\\WinMerge-2.8.4-exe\\WinMergeU.exe"

def check_parameters():
    "check if your parameters are right"
    if len(sys.argv) < 3:
        print "usage: {} FILE FIRST_BRANCH SECOND_BRANCH".format(sys.argv[0])
        sys.exit(0)

    the_file = sys.argv[3]
    if not os.path.isfile(the_file):
        print "File {} does not exist.".format(the_file)
        sys.exit(0)

def obtin_files(the_file, first_branch, second_branch):
    "get from git the two files which will be compared"
    os.rename(the_file, the_file + ".tmp")

    mask = "/tmp/{}.{}.{}".format(the_file, "{}",
    	of.get_file_extension(the_file))
    first_file = mask.format(first_branch.replace("/","_"))
    second_file = mask.format(second_branch.replace("/","_"))

    subprocess.check_output(["git", "checkout", first_branch , the_file])
    os.rename(the_file, first_file)

    subprocess.check_output(["git", "checkout", second_branch , the_file])
    os.rename(the_file, second_file)
    os.rename(the_file + ".tmp", the_file)

    return first_file , second_file

def main():
    "main()... duhh"
    check_parameters()
    the_file = sys.argv[3]
    first_branch = sys.argv[1]
    second_branch = sys.argv[2]
    first_file, second_file = obtin_files(the_file, first_branch, second_branch)

    first_path = of.convert_path(first_file)
    second_path = of.convert_path(second_file)

    the_command = "{} {} {}".format(WINMERGE, first_path, second_path)
    of.send_socket_cmd(the_command)


if __name__ == "__main__":
    main()

