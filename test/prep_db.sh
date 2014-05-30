#!/bin/bash

sqlite3 ../monitor.db ".read ../db.sql"
sqlite3 ../monitor.db "INSERT INTO USERS VALUES('user1', 'passw0rd')"
