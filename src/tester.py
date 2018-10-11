from models import League, Team
from tabulate import tabulate
from game import Game, GameResult
import game
from os import system
import json, rostertool, sys, random

l = rostertool.loadLeague("USFL")
t1 = l.getTeam("Boston")
t2 = l.getTeam("New Jersey")

t1_wins = 0
t2_wins = 0

N = 100

for i in range(N):
	g = Game(t1, t2)
	gr = g.playGame()
	if(gr.winner == t1.teamName):
		t1_wins += 1
	else:
		t2_wins += 1

print("t1 %d t2 %d") % (t1_wins, t2_wins)
print("t1 pct %.1f") % (float(t1_wins)/N*100)
