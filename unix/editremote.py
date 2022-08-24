#!/usr/bin/env python3
import sys
import logging
import tempfile
import os
import os.path
import subprocess
import time
import shutil

#pip install watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class LocalRemoteFile(FileSystemEventHandler):
    def __init__(self, remotefile, ssh_key=None):
        self.ssh_key = ssh_key
        self.remotefile = remotefile
        self.generate_temp_file()
        self.copy_remote_file_here()

    def copy_remote_file_here(self):
        self.copy_file(self.remotefile, self.localfile)

    def copy_local_file_remote(self):
        self.copy_file(self.localfile, self.remotefile)

    def copy_file(self, source_file, target_file):
        print("Copying {} to {}".format(source_file, target_file))
        if self.ssh_key:
            cmd = ["scp", "-i", self.ssh_key, source_file, target_file]
        else:
            cmd = ["scp", source_file, target_file]
        try:
            subprocess.check_output(cmd)
        except:
            pass

    def generate_temp_file(self):
        pos = self.remotefile.find(":")
        if pos < 0:
            print("error: invalid SSH path [{}]".format(self.remotefile))
            sys.exit(1)
        remote_path = self.remotefile[pos+1:]
        basepath = os.path.basename(remote_path)
        self.tempfolder = tempfile.mkdtemp()
        self.localfile = os.path.join(self.tempfolder, basepath)

    def on_modified(self, event):
        if event.is_directory:
            return
        self.copy_local_file_remote()

def usage():
    print("""
    copies the remote file here, open with an editor, watch for signals and sent it back to it's source every time it's update.
    the easiest way to edit remote files locally, even better if they are on the other side of the planet and the latency is annoying.

    usage:   {0} login@server:/full/path/of/a/file/you/want/to/edit
    usage:   {0} -i ~/some_key login@server:/full/path/of/a/file/you/want/to/edit
    example: {0} john@myserver.com:/tmp/blah.txt
    """.format(sys.argv[0]))

def doit():
    import sys
    import time
    import logging
    from watchdog.observers import Observer
    from watchdog.events import LoggingEventHandler

    if __name__ == "__main__":
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        path = sys.argv[1] if len(sys.argv) > 1 else '.'
        event_handler = MyEventHandler() # LoggingEventHandler()
        observer = Observer()
        observer.schedule(event_handler, path, recursive=False)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


def go(target_file, ssh_key=None):
    print("Copying file...")
    event_handler = LocalRemoteFile(target_file, ssh_key)
    observer = Observer()
    observer.schedule(event_handler, event_handler.tempfolder, recursive=False)
    observer.start()
    print("Editing File")
    subprocess.check_output(["of", event_handler.localfile])
    print("Waiting For Events...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print("Erasing Temporary Directory")
    shutil.rmtree(event_handler.tempfolder)
    print("Done")

def main():
    args = len(sys.argv)
    if args == 2:
        target_file = sys.argv[1]
        return go(target_file)
    if args == 4 and sys.argv[1] == "-i":
        ssh_key = sys.argv[2]
        target_file = sys.argv[3]
        return go(target_file, ssh_key)
    return usage()


if __name__ == "__main__":
    main()
