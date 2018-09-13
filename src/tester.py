from models import League, Team
from tabulate import tabulate
from os import system
import json, rostertool, sys

# leagueName = "USFL"
# teamNames = ["Boston","New York","Philadelphia","New Jersey",
# "Washington","Miami","Chicago","Cleveland",
# "Los Angeles","San Francisco","San Diego","Seattle",
# "Texas","Colorado","Phoenix","San Antonio"]

# teamRoster = {}

# for name in teamNames:
# 	roster = []
# 	for i in range(3):
# 		roster.append(rostertool.createRandomPlayer(70,99))
# 	for i in range(3):
# 		roster.append(rostertool.createRandomPlayer(60,87))
# 	for i in range(4):
# 		roster.append(rostertool.createRandomPlayer(50,83))
# 	team = Team(name, roster)
# 	teamRoster[team.teamName] = team

# league = League(leagueName, teamRoster)
# rostertool.writeLeague(league)

def printHeader(teamname):
	print ("--------------------------------------")
	print (teamname)
	print("--------------------------------------")

system("clear")
league = rostertool.loadLeague(sys.argv[1])
while(True):
	inp = raw_input(">").rstrip().lstrip()
	system("clear")
	if(inp == "quit"):
		break
	team = league.getTeam(inp)
	t = []
	for player in team.roster:
		t.append([player.fullName(), player.offense, player.defense])
	printHeader(team.teamName)
	print tabulate(t,["Name","Offense","Defense"])
	print ""
