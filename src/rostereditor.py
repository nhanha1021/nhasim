import sys, rostertool
from models import League, Team, Player
from tabulate import tabulate
from os import system

league = None

def getInput():
	inp = raw_input(">")
	inp = inp.rstrip().lstrip()
	cmd = inp.split(' ')
	return cmd

def init():
	system("clear")
	global league
	league = rostertool.loadLeague(sys.argv[1])

def printTeamRoster(teamName):
	team = league.getTeam(teamName)
	table = []
	for player in team.roster:
		table.append([player.fullName(),player.offense,player.defense])
	print tabulate(table, ["Name","Offense","Defense"])

def printTeamNames():
	for name in league.teamRoster.keys():
		print name

def help():
	table = []
	table.append(["roster X","Display the roster of team X"])
	table.append(["teams","Display the name of each team in the league"])
	table.append(["quit","Quit the program"])
	table.append(["help","Display the list of commands"])
	print tabulate(table, ["Command", "Description"])

init()
while(True):
	cmd = getInput()
	if(cmd[0] == "roster"):
		system("clear")
		printTeamRoster(cmd[1].replace("_"," "))
	if(cmd[0] == "teams"):
		system("clear")
		printTeamNames()
	if(cmd[0] == "help"):
		system("clear")
		help()
	if(cmd[0] == "quit"):
		break
	print ""



