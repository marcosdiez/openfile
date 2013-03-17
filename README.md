
 OpenFile
===========
OpenFile is a set of scripts to close the gap of developing on Linux in a Windows box.

##The Problem

- Unix is an awesome development environment, but the UI is not.
- Windows has a nice UI and works with my hardware but is not good for programming.
- Mac has only the disadvantages above (any many others).

##The Objective


To have Windows on my computer, but with a *real* Unix shell (not cygwin) instead of *cmd.exe*.

##The solution


* Have Windows installed as your main OS
* Install Unix on another machine (or a Virtual Machine )
* Make sure both machines connect with each other though IP ( NAT or BRIDGE )
* Share your Unix homedir and /tmp with Windows thought **samba** ( mine are z: and x:, respectively )
* Use **putty** to connect to your Unix box, authenticating though ssh keys so you *never* have to type any password
* Use the scripts in this package to close the gab

##The Script


The script is called **of**, which means both *openfile* and *openfolder*. It opens files and folder located in the Unix box on the Windows machine, just like **start.exe** (technical explanation later)


Examples:

If you type (on your Unix box, though putty):

    $pwd
    /home/marcos/folder1/folder2

    $of
    (opens Z:\folder1\folder2 on Windows Explorer)

    $of anotherfolder
    (opens Z:\folder1\folder2\anotherfolder on Windows Explorer)

    $of ..
    (opens Z:\folder1 on Windows Explorer)

    $of ../../../..
    (gives you an error)

    $of /tmp
    (opens X:\)

    $of /tmp/blah.txt
    (opens X:\blah.txt on Windows with the associated editor ( notepad.exe )
    (notepad++.exe or sublime text if you did your homework properly)

    $of myapp/somescript.py
    (opens Z:\folder1\folder2\myapp\myscript.py on the default editor)

    $of myspreadsheet.xlsx
    (opens z:\folder1\folder2\myspreadsheet.xlsx with Excel or OpenOffice)

    **bonus**
    $of # File "/home/marcos/3s/code/.envGama/src/django/django/core/servers/basehttp.py", line 139, in __init__
    (open z:\3s\code\.engGama\src\django\django\core\servers\basehttp.py on line 139)


## How it works

The only possible way: it is necessary to run a C# server on Windows which accepts and runs remote commands from the Unix box.

It is actually not insecure if used properly (yes, it was made to be used by adults). Whenever on runs **of**, it sends the request to the IP which connected to the virtual terminal. The server will receive the request and pop up on the an UI saying that it received a request. If you click on accept, it will start trusting this IP address.
To improve security:

* you can only trust on IP at a time (i.e. trusting another IP will make it automatically untrusts the former IP)
* it does not save the trusted IP anywhere, so if you restart the program it will ask it again.


That means the tool is safe as long as you are not running nasty code **AND** you are the only person on the unix box.


## What comes in the package

* smb.conf
* the **of** shell script
* the C# server (compiled and source)
* this documentation


## Known Bugs

As the following settings were used on smb.conf
    create mask = 0644
every time one edits a file on Windows it stops being executable on unix. The solution for that would be writing a daemon that listen to filesystem changes and chmod the files automatically.



## Meta
Created by Marcos Diez < marcos AT unitron.com.br >
Released under the MIT License: http://www.opensource.org/licenses/mit-license.php
http://github.com/marcosdiez/openfile

