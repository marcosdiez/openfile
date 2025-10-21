#!/bin/bash
set -x -e
go fmt
rm -vf FolderOpener.exe


# GOOS=windows GOARCH=amd64 go build
GOOS=windows GOARCH=amd64 go build -ldflags="-H windowsgui"

