from models import League, Team
from tabulate import tabulate
from game import Game, GameResult
import game
from os import system
import json, rostertool, sys, random

def eventfilter(events):
	table = []
	for event in events:
		for entry in table:
			if(entry[0] == event.playername):
				entry[1] += event.point
				break
		else:
			table.append([event.playername, event.point])
	return table

l = rostertool.loadLeague("USFL")
at = l.getTeam("Boston")
ht = l.getTeam("New Jersey")

g = Game(at, ht)
gr = g.playGame()

print gr.atname, gr.atscore, gr.htname, gr.htscore
print ""
for entry in eventfilter(gr.atevents):
	print entry[0], entry[1]
print ""
for entry in eventfilter(gr.htevents):
	print entry[0], entry[1]



