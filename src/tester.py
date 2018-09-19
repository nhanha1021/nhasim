from models import League, Team
from tabulate import tabulate
from os import system
import json, rostertool, sys

league = rostertool.loadLeague("USFL")
team = league.getTeam("Boston")
for key in team.roster.keys():
	print key

print ""
for player in team.allPlayers():
	print player.fullName()
print ""

p1 = team.getPlayer("Charles Patton")
p2 = team.getPlayer("CharlesPatton")
p3 = team.getPlayer("charles patton")
p4 = team.getPlayer("charlespatton")
p5 = team.getPlayer("ChaRleSpaTToN")

print p1.fullName()
print p2.fullName()
print p3.fullName()
print p4.fullName()
print p5.fullName()

# def overallOff(team):
# 	s = sum(player.offense for player in team.roster)
# 	print int(s/len(team.roster))

# def overallDef(team):
# 	s = sum(player.defense for player in team.roster)
# 	print int(s/len(team.roster))

# league = rostertool.loadLeague("USFL")

# for team in league.allTeams():
# 	print team.teamName
# 	overallOff(team)
# 	overallDef(team)
# 	print ""