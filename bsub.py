#!/usr/bin/python
from itertools import islice
from subprocess import Popen
import sys
import os

NCPUS = 3 # max number of used CPUs at a moment, no more than 2 concurrent processes

if len(sys.argv) != 2:
	print("\nbsub.py submit locally a list of commands and manages them over CPUs")
	print("\n\033[1;33m Example: ./bsub.py list_of_commands.txt\033[0m\n")
	print("\t\tlist_of_commands.txt: contains one command per line")
	if(len(sys.argv)!=2):
		sys.exit("\n\033[1;31m ERROR: please provide one argument corresponding to the file with commands\033[0m\n")

nameOfCommandFile = sys.argv[1]

test = os.path.isfile(nameOfCommandFile)
if test == False:
	sys.exit("\n\033[1;31m ERROR: file '{0}' is not found\033[0m\n".format(nameOfCommandFile))

commands = []
infile = open(nameOfCommandFile, "r")
for i in infile:
	commands.append(i.strip())



max_workers = NCPUS # max number of used CPUs at a moment, no more than 2 concurrent processes
processes = (Popen(cmd, shell=True) for cmd in commands)
running_processes = list(islice(processes, max_workers))  # start new processes
while running_processes:
	for i, process in enumerate(running_processes):
		if process.poll() is not None:  # the process has finished
			running_processes[i] = next(processes, None)  # start new process
			if running_processes[i] is None: # no new processes
				del running_processes[i]
				break

