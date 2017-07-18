 OpenFile
===========
**OpenFile** is a set of scripts to close the gap of developing on Linux in a Windows box.

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
* Share your Unix / folder with Windows thought **samba** ( mine is z: )
* Use **putty** to connect to your Unix box, authenticating through ssh keys so you *never* have to type any password
* on Windows, run FolderOpener2.exe, which is the server that handles requests from Linux
* on Linux, run of.py and the other python scripts. It's even more fun if you put them on your PATH
* you may want to edit of.py to change the path of the openers. Since spaces don't work well, use *dir /X* to get the 8 chars folder names


##An alternative solution if you use Windows 10 with Microsoft Subsystem for Linux (bash on Ubuntu on Windows)

* use Windows 10 with "bash on Ubuntu on Windows"
* on Windows, run FolderOpener2.exe, which is the server that handles requests from Linux
* on bash, run of.py and the other python scripts. It's even more fun if you put them on your PATH
* you may want to edit of.py to change the path of the openers. Since spaces don't work well, use *dir /X* to get the 8 chars folder names


##The Script


The script is called **of**, which means both *openfile* and *openfolder*. It opens files and folders located in the Unix box on the Windows machine, just like **start.exe** (technical explanation later). It also launches websites from the unix box in the Windows browser


Examples:

If you type (on your Unix box, though putty):

    $pwd
    #/home/marcos/folder1/folder2

    $of
    #opens Z:\home\marcos\folder1\folder2 on Windows Explorer

    $of anotherfolder
    #opens Z:\home\marcos\folder1\folder2\anotherfolder on Windows Explorer

    $of http://google.com
    #opens http://google.com on Windows' default internet browser

    $of https://google.com
    #opens https://google.com on Windows' default internet browser

    $of ..
    #opens Z:\home\marcos\folder1 on Windows Explorer

    $of ../../../../../../../../
    #gives you an error

    $of /tmp
    #opens z:/tmp

    $of /tmp/blah.txt
    #opens z:\tmp\blah.txt on Windows with the associated editor ( notepad.exe )
    #or microsoft visual studio code if you did your homework properly

    $of myapp/somescript.py
    #opens Z:\home\marcos\folder1\folder2\myapp\myscript.py on Windows with the associated editor

    $of myspreadsheet.xlsx
    #opens Z:\home\marcos\folder1\folder2\myapp\myspreadsheet.xlsx on Windows with the associated editor (Excel/OpenOffice)

    **bonus**
    $of  File "/home/marcos/3s/code/.envGama/src/django/django/core/servers/basehttp.py", line 139, in __init__
    #open z:\home\marcos\3s\code\.engGama\src\django\django\core\servers\basehttp.py on line 139

    $of  "/home/marcos/3s/code/.envGama/src/django/django/core/servers/basehttp.py", line 139, in __init__
    #open z:\home\marcos\3s\code\.engGama\src\django\django\core\servers\basehttp.py on line 139


## How it works

It is necessary to run a C# server on Windows which accepts and runs remote commands from the Unix box.

It is actually not insecure if used properly (yes, it was made to be used by adults). Whenever one runs **of**, it sends the request to the IP which is connected to the virtual terminal (obtained via `who`). The server will receive the request and pop up on the an UI saying that it received a request. If you click on accept, it will start trusting this IP address.
Some basic security features:

* it only trusts one IP at a time (i.e. trusting another IP will automatically untrust the former IP)
* it does not save the trusted IP anywhere, so if you restart the program it will ask it again.


That means the tool is safe as long as you are not running nasty code **AND** you are the only person on the unix box.


## What comes in the package

* smb.conf
* the `of.py` python script
* the C# server (compiled and source) # no install and no config, just click and run!
* this documentation

## Settings

I recommend uncommenting the following lines on `of`
  ALTERNATIVEOPENER="c:\progra~1\sublim~1\sublim~1.exe"
as the default editor is wordpad.exe ( common denonimator )
Also, you must change your folder paths on `of` (  z: is / as default )



## merger

merger is a tool that uses openfile so one can use winmerge to see diference between branches


usage: ./merger.py FIRST_BRANCH SECOND_BRANCH FILE

opens WinMerge to compare the file from both branches


## Meta
Created by Marcos Diez < marcos AT unitron.com.br >
Released under the MIT License: http://www.opensource.org/licenses/mit-license.php
http://github.com/marcosdiez/openfile


Icon by http://www.creativefreedom.co.uk/ ( http://www.iconfinder.com/icondetails/61771/48/folder_icon )

