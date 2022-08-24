#!/usr/bin/env python
import sys
import os
import os.path

import of

MELD_PATH = """c:\\progra~2\\Meld\\Meld.exe"""

def usage():
    print "usage: meld.py FIRST_FILE SECOND_FILE THIRD_FILE"

def expect_file_to_exist(filename):
    if not os.path.isfile(filename):
        print "error: [{}] does not exist".format(filename)
        sys.exit(1)

def launch_meld(first_file, second_file, third_file):
    expect_file_to_exist(first_file)
    expect_file_to_exist(second_file)
    expect_file_to_exist(third_file)
    converted_first_file = of.convert_path(first_file)
    converted_second_file = of.convert_path(second_file)
    converted_third_file = of.convert_path(third_file)

    final_command = """{} "{}" "{}" "{}" """.format(
        MELD_PATH,
        converted_first_file,
        converted_second_file,
        converted_third_file
    )
    of.send_socket_cmd(final_command)

def main():
    #no parameter, we open the current folder
    if len(sys.argv) != 4:
        usage()
        sys.exit(1)

    first_file = sys.argv[1]
    second_file = sys.argv[2]
    third_file = sys.argv[3]

    launch_meld(first_file, second_file, third_file)


if __name__ == "__main__":
    main()
