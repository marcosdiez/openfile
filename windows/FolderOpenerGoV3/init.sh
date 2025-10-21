#!/bin/bash
go mod init github.com/marcosdiez/openfile/FolderOpenerV3;
go mod tidy
2goarray icon main < FolderOpenerV3.ico > icon.go
rsrc -manifest FolderOpenerV3.manifest -ico FolderOpenerV3.ico -o rsrc.syso


# https://github.com/cratonica/2goarray
# https://github.com/akavel/rsrc