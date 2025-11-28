#!/usr/bin/env python3

import sys
import os
import os.path

def show_paths():
    uid = os.getuid()
    folder = "/proc"
    blacklist = [ "/proc/net" , "/proc/self", "/proc/thread-self" ]
    boring_paths =  ["/", os.path.expanduser("~")]
    output = []
    for proc_path in os.scandir(folder):
        try:
            if not proc_path.is_dir():
                continue
            if proc_path.stat().st_uid != uid:
                continue
            if proc_path.path in blacklist:
                continue
            cwd = "{}/cwd".format(proc_path.path)
            try:
                cwd_value = os.readlink(cwd)
            except PermissionError:
                continue
            if cwd_value in boring_paths:
                continue
            if cwd_value not in output:
                output.append(cwd_value)
        except FileNotFoundError:
            # that means we got a race condition and the PID stopped
            # happening existing during the loop
            continue
    return output

def max_length(the_list):
    max_length = 0
    for elem in the_list:
        this_length = len(elem)
        if this_length > max_length:
            max_length = this_length
    return max_length



if len(sys.argv) < 2:
    print("This program shows the path in which each bash is located, so you can easily go to the same path in a different terminal")
    print("")
    paths = show_paths()
    length = max_length(paths)
    mask = "cd {path:" + str(length) + "}   #   {counter}"
    counter = 0
    for path in paths:
        print(mask.format(counter=counter, path=path))
        counter += 1
    print("")
    sys.exit(1)
else:
    n = int(sys.argv[1])
    print(show_paths()[n])