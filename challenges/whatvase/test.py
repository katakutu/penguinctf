#!/usr/bin/python

import sys

sys.stdout.write("A: ")
sys.stdout.flush()
data = sys.stdin.readline()
sys.stdout.write("Received: %s" % data)
