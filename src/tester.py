from models import League, Team
from tabulate import tabulate
from os import system
import json, rostertool, sys

table = []
table.append(["Dogs",3])
table.append(["DogsDogsDogs", 44])

t = tabulate(table)
header = ""
for i in range(len(t)):
	header += "-"

j = len(t.split("\n")[0])
header = ""
for i in range(j):
	header +="="

print header
print t