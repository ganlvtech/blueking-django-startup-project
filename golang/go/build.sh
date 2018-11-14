#!/usr/bin/env bash
pushd src/
export GOOS=linux
go build -o ../bin/main
export GOOS=windows
go build -o ../bin/main.exe
export GOOS=
popd
