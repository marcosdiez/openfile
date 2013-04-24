#!/usr/bin/env python
import subprocess
import sys
import re
import os
import os.path
import socket
#settings

TARGET_PORT = 9998

replace_path = [
	[os.environ.get('HOME') + "/tmp" , "z:\\tmp"] ,
	["/tmp" , "x:\\"] ,
	[os.environ.get('HOME') , "z:"] ,
	["/" , "\\"] ,
]

ALTERNATIVEOPENER="c:\progra~1\sublim~1\sublim~1.exe"
DEFAULTOPENER=ALTERNATIVEOPENER

#the ALTERNATIVEOPENER will be used for files without extensions (README, .bashrc, etc...)
#ALTERNATIVEOPENER="wordpad.exe"
#the default opener will use windows associations. I actually use sublime edit for everything.
#DEFAULTOPENER=""


#################################################
def main():
	#no parameter, we open the current folder
	if len(sys.argv) == 1:
		open_url(os.getcwd())
		return

	if sys.argv[1] in ( "-h" , "--help" , "-help" ):
		usage()
		return

	if sys.argv[1] == "File" and not os.path.exists("File"):
		del sys.argv[1]

	if sys.argv[2] == "line" and not os.path.exists("line"):
		#now this is for python errors, like File "/home/marcos/3s/code/.envGama/src/django/django/core/servers/basehttp.py", line 139, in __init__
		open_url(sys.argv[1] + ":" + sys.argv[2].replace(",",""))
		return

	for parameter in sys.argv[1:]:
		open_url(parameter)
	return


def open_url(target_url):
	if os.path.isdir(target_url):
		opendir(target_url)
		return

	if os.path.isfile(target_url):
		openfile(target_url)
		return

	#files that have a column and a number followed by should be interpreted as line numbers
	cln = target_url.find(":")
	if cln > 0:
		new_url = target_url[0:cln]
		if os.path.isfile(new_url):
			openfile(target_url) #this is not a bug. some editors will open README:22 on line 22 :)
			return

	target_url = sys.argv[1][0:-1]
	if os.path.isfile(target_url):
		sys.argv[3]=sys.argv[3].replace(",","")
		openfile(target_url+":"+sys.argv[3])
		return

	print "Error: File/Dir [%s] does not exist." % target_url

def opendir(the_path):
	send_socket_cmd(convert_path(the_path))

def get_file_extension(the_path):
	last_dot=the_path.rfind(".")
	return the_path[last_dot+1:].lower()

def openfile(the_path):
	last_slash=the_path.rfind("/")
	last_dot=the_path.rfind(".")

	if last_dot == -1 or last_slash > last_dot or last_dot == len(the_path)-1:
		opener = ALTERNATIVEOPENER
	else:
		extension = get_file_extension(the_path)
		if extension in ( "mp3", "xml" , "xlsx" , "doc" , "docx" , "jpg" , "png" , "ico" ):
			opener = ""
		else:
			opener = DEFAULTOPENER

	the_path = opener + " " + convert_path(the_path)
	send_socket_cmd(the_path)

def send_socket_cmd(msg):
	msg = msg.strip()
	print msg
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((server_ip(), TARGET_PORT))
	totalsent = 0
	msglen=len(msg)
	while totalsent < msglen:
		sent = sock.send(msg[totalsent:])
		if sent == 0:
			raise RuntimeError("socket connection broken")
		totalsent = totalsent + sent

def make_absolute_path_if_necessary(the_path):
	if the_path[0] == "/":
		return the_path
	return os.getcwd() + "/" + the_path

def convert_path(the_path):
	return path_replaced(make_absolute_path_if_necessary(the_path))

def path_replaced(the_path):
	for replace_pair in replace_path:
		the_path = the_path.replace(replace_pair[0], replace_pair[1])
	return the_path

def server_ip():
	#IP=`who --ips -m|egrep -o --color=no   "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+"`
	output = subprocess.check_output(["who", "--ips", "-m"])
	m = re.search("\d+\.\d+.\d+.\d+" , output)
	return m.group(0)

def usage():
	print """Opens Folders and Files on the remote machine.
usage:

of /tmp/blah.txt
of somefolder"
of somefolder/otherfolder/blah.xls
of File "/home/marcos/3s/code/.envGama/src/django/django/core/servers/basehttp.py", line 139, in __init__ #open on line 139
of "/home/marcos/3s/code/.envGama/src/django/django/core/servers/basehttp.py", line 139, in __init__ #open on line 139
"""

if __name__=="__main__":
	main()
