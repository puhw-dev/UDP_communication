#!/bin/bash

grep -c "Communication started" ../logs/client*
grep -c "Message sent" ../logs/client*
grep -c "Message received" ../logs/server*
grep -c "UnknownMessageType" ../logs/server*
