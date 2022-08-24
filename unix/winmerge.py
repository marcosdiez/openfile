#!/usr/bin/env python3
import sys
import os
import os.path
import hashlib
import of

WINMERGE_PATH = """c:\\progs\\WinMerge-2.8.4-exe\\WinMergeU.exe"""
MELD_PATH =  """c:\\progs\\WinMerge\\WinMergeU.exe""" # """c:\\progra~2\\Meld\\Meld.exe"""


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def usage():
    print("usage: winmerge.py FIRST_FILE SECOND_FILE [THIRD_FILE]")

def expect_file_to_exist(filename_or_folder):
    if os.path.isfile(filename_or_folder) or os.path.isdir(filename_or_folder):
        return True
    print("error: [{}] does not exist".format(filename_or_folder))
    sys.exit(1)

def launch_winmerge(first_file, second_file):
    expect_file_to_exist(first_file)
    expect_file_to_exist(second_file)
    converted_first_file = of.convert_path(first_file)
    converted_second_file = of.convert_path(second_file)

    final_command = """{} "{}" "{}" """.format(
    	WINMERGE_PATH, converted_first_file, converted_second_file)
    of.send_socket_cmd(final_command)

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
    num_parameters = len(sys.argv)
    if num_parameters == 3:
        if not os.path.isdir(sys.argv[1]) and md5(sys.argv[1]) == md5(sys.argv[2]):
            print("Error: both files are the same. No point in opening them with WinMerge")
        else:
            launch_winmerge(sys.argv[1], sys.argv[2])
    elif num_parameters == 4:
        if not os.path.isdir(sys.argv[1]) and md5(sys.argv[1]) == md5(sys.argv[2]) and md5(sys.argv[1]) == md5(sys.argv[3]):
            print("Error: all files are the same. No point in opening them with WinMerge")
        else:
            launch_meld(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
