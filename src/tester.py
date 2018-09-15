from models import League, Team
from tabulate import tabulate
from os import system
import json, rostertool, sys

inp = raw_input("\n")
inp = inp.rstrip().lstrip()
cmd = inp.split('.')
for i in range(len(cmd)):
	cmd[i] = cmd[i].rstrip().lstrip()
	print cmd[i]



