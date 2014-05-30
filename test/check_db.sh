#!/bin/bash

sqlite3 ../monitor.db "select * from sensor"
sqlite3 ../monitor.db "select * from metric"
