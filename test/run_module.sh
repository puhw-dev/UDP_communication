#!/bin/bash

gnome-terminal --tab -e "./../src/server.py"
sleep 2
gnome-terminal --tab -e "./../src/client.py"
sleep 2
pid=$( pgrep server.py )
kill -9 $pid

