#!/usr/bin/env python
from __future__ import unicode_literals

import time
import subprocess
import sys
import re
import os
import os.path
import socket
# settings

TARGET_PORT = 9998

REPLACE_PATH = [
    ["/mnt/c/", "c:\\"], # microsoft linux
    ["/mnt/d/", "d:\\"], # microsoft linux
    ["/mnt/e/", "e:\\"], # microsoft linux
    ["/mnt/f/", "f:\\"], # microsoft linux
    ["/", "z:\\"],
]



openers = {
    "androidstudio": {
        "path": """C:\\Users\\Marcos\\AppData\\Local\\Android\\android-studio\\bin\\studio64.exe""",
        "open_with_line_number_cmd": "{opener} --line {line_number} \"{file_path}\"",
        "open_without_line_number_cmd": "{opener} \"{file_path}\""
    },
    "pycharm": {
        "path": """C:\\Progra~2\\JetBrains\\PYCHAR~1.2\\bin\\pycharm.exe""",
        "open_with_line_number_cmd": "{opener} {project_folder} --line {line_number} \"{file_path}\"",
        "open_without_line_number_cmd": "{opener} {project_folder} \"{file_path}\""
    },
    "mscode": {
        "path": """c:\\progra~2\\mifa7f~1\\code.exe""",
        "open_with_line_number_cmd": "{opener} -g -r \"{file_path}\":{line_number} ",
        "open_without_line_number_cmd": "{opener} -r \"{file_path}\""
    },
    "explorer": {
        "path": "explorer.exe",
        "open_with_line_number_cmd": '{opener} "{file_path}"',
        "open_without_line_number_cmd": '{opener} "{file_path}"',
    },
    "audacity": {
        "path": "c:\\Progra~2\\Audacity\\audacity.exe",
        "open_with_line_number_cmd": '{opener} "{file_path}"',
        "open_without_line_number_cmd": '{opener} "{file_path}"',
    }

}

open_associations = {
    ".py": openers["pycharm"],
    ".mp3": openers["explorer"],
    ".xls": openers["explorer"],
    ".xlsx": openers["explorer"],
    ".doc": openers["explorer"],
    ".docx": openers["explorer"],
    ".jpg": openers["explorer"],
    ".png": openers["explorer"],
    ".ico": openers["explorer"],
    ".sqlite3": openers["explorer"],
    ".pdf": openers["explorer"],
    ".java": openers["androidstudio"],
    ".wav": openers["audacity"],
    "*": openers["mscode"],
}

#the ALTERNATIVEOPENER will be used for files without extensions (README, .bashrc, etc...)
#ALTERNATIVEOPENER="wordpad.exe"
#the default opener will use windows associations. I actually use sublime edit for everything.
#DEFAULTOPENER = ""


#################################################
def main():
    #no parameter, we open the current folder
    if len(sys.argv) == 1:
        open_url(os.getcwd())
        return

    if sys.argv[1] in ( "-h", "--help", "-help" ):
        usage()
        return

    parse_user_defined_opener()

    if sys.argv[1] == "File" and not os.path.exists("File"):
        del sys.argv[1]

    if len(sys.argv) > 2 and sys.argv[2] == "line" and not os.path.exists("line"):
        #now this is for python errors, like

        # File "/home/marcos/3s/code/.envGama/src/django/django/core/servers/basehttp.py", line 139, in __init__
        line_number = sys.argv[3].replace(",", "")
        the_file = sys.argv[1].replace(",", "")
        openfile(the_file, line_number)
        return

    first = True
    for parameter in sys.argv[1:]:
        if first:
            first = False
        else:
            #time.sleep(3)
            pass
        open_url(parameter)
    return


def parse_user_defined_opener():
    global USER_DEFINED_OPENER
    magic_string = "--opener="
    counter = 0
    for argv in sys.argv:
        if argv.find(magic_string) == 0:
            del sys.argv[counter]
            USER_DEFINED_OPENER = argv[len(magic_string):]
            return
        counter += 1


def open_url(target_url):
    if is_internet_address(target_url):
        send_socket_cmd(target_url)
        return

    if os.path.isdir(target_url):
        opendir(target_url)
        return

    if os.path.isfile(target_url):
        openfile(target_url)
        return

    #files that have a column and a number followed by should be interpreted as line numbers
    cln = target_url.find(":")
    if cln > 0:
        file_name = target_url[0:cln]
        if os.path.isfile(file_name):
            line_number = target_url[cln + 1:]
            openfile(file_name, line_number)
            return

    target_url = sys.argv[1][0:-1]
    if os.path.isfile(target_url):
        line_number = sys.argv[3].replace(",", "")
        openfile(target_url, line_number)
        return

    print "Error: File/Dir [%s] does not exist." % target_url


def is_internet_address(target_url):
    return target_url.find("http://") == 0 or target_url.find("https://") == 0


def opendir(the_path):
    send_socket_cmd(convert_path(the_path))


def convert_path(the_path):
    return path_replaced(make_absolute_path_if_necessary(the_path))


def get_file_extension(the_path):
    last_dot = the_path.rfind(".")
    return the_path[last_dot + 1:].lower()


def openfile(the_path, line_number=None):
    last_dot = the_path.rfind(".")
    extension = the_path[last_dot:]

    if extension in open_associations:
        opener = open_associations[extension]
    else:
        opener = open_associations["*"]

    if line_number is None:
        cmd = opener["open_without_line_number_cmd"]
    else:
        cmd = opener["open_with_line_number_cmd"]

    the_path = make_absolute_path_if_necessary(the_path)

    project_folder = path_replaced(get_project_folder(the_path))
    file_path = path_replaced(the_path)

    the_cmd = cmd.format(opener=opener["path"],
                         file_path=file_path,
                         line_number=line_number,
                         project_folder=project_folder
                         )
    send_socket_cmd(the_cmd)

def get_project_folder(file_path):
    # this is ridiculous
    # a PyCharm project stais under a .idea folder
    # so I have to look for the folder in order for pycharm to work as expected
    folder = os.path.dirname(file_path)

    while True:
        if os.path.isdir(os.path.join(folder, ".idea")):
            return folder

        pos = folder.rfind("/")
        if pos < 1:
            break
        folder = folder[0:pos]

    return ""

def send_socket_cmd(msg):
    msg = msg.strip()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip(), TARGET_PORT))
    totalsent = 0
    msglen = len(msg)
    while totalsent < msglen:
        sent = sock.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent





def make_absolute_path_if_necessary(the_path):
    if the_path[0] == "/":
        return the_path
    return os.getcwd() + "/" + the_path


def path_replaced(the_path):
    old_path = the_path
    for replace_pair in REPLACE_PATH:
        if replace_pair[0] in the_path:
            the_path = the_path.replace(replace_pair[0], replace_pair[1], 1)
            break
    the_path = the_path.replace(os.sep, "\\")
    print "{} -- {} -> {}".format(server_ip(), old_path, the_path)
    return the_path


def is_microsoft_linux():
    with file("/proc/version") as f:
        file_content = f.read()
        return "Microsoft" in file_content
    return False


def server_ip():
    if is_microsoft_linux():
        return "127.0.0.1"
    #IP=`who --ips -m|egrep -o --color=no   "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+"`
    output = subprocess.check_output(["who", "--ips", "-m"])
    the_ip = re.search("\\d+\\.\\d+.\\d+.\\d+", output)
    return the_ip.group(0)


def usage():
    """explains how to use the program"""

    print """Opens Folders and Files on the remote machine.
usage:

of /tmp/blah.txt
of somefolder"
of somefolder/otherfolder/blah.xls
of File "/home/marcos/3s/code/.envGama/src/django/django/core/servers/basehttp.py", line 139, in __init__ #open on line 139
of "/home/marcos/3s/code/.envGama/src/django/django/core/servers/basehttp.py", line 139, in __init__ #open on line 139

"""


if __name__ == "__main__":
    main()
