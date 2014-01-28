#!/usr/bin/env python
import sys
import os
import os.path

import of

WINMERGE_PATH = """c:\\progs\\WinMerge-2.8.4-exe\\WinMergeU.exe"""

def usage():
    print "usage: winmerge FIRST_FILE SECOND_FILE"

def expect_file_to_exist(filename):
    if not os.path.isfile(filename):
        print "error: [{}] does not exist".format(filename)
        sys.exit(1)

def launch_winmerge(first_file, second_file):
    expect_file_to_exist(first_file)
    expect_file_to_exist(second_file)
    converted_first_file = of.convert_path(first_file)
    converted_second_file = of.convert_path(second_file)

    final_command = """{} "{}" "{}" """.format(
    	WINMERGE_PATH, converted_first_file, converted_second_file)
    of.send_socket_cmd(final_command)

def main():
    #no parameter, we open the current folder
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)

    first_file = sys.argv[1]
    second_file = sys.argv[2]

    launch_winmerge(first_file, second_file)


if __name__ == "__main__":
    main()
