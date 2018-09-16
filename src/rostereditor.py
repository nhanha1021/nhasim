import sys, rostertool
from models import League, Team, Player
from tabulate import tabulate
from os import system

def getInput():
	inp = raw_input("\n")
	inp = inp.rstrip().lstrip()
	cmd = inp.split('.')
	for i in range(len(cmd)):
		cmd[i] = cmd[i].rstrip().lstrip()
	return cmd

def init():
	system("clear")
	league = rostertool.loadLeague(sys.argv[1])
	return MainShell(league)

class MainShell(object):

	def __init__(self, league):
		self.league = league

	def run(self):
		while(True):
			system("clear")
			self.printTeams()
			cmd = getInput()
			if(cmd[0] == "add"):
				self.add(cmd[1])
			if(cmd[0] == "rm"):
				self.rm(cmd[1])
			if(cmd[0] == "view"):
				ts = TeamShell(self.league.getTeam(cmd[1]))
				ts.run()
			if(cmd[0] == "quit"):
				break

	def printTeams(self):
		for name in self.league.teamRoster.keys():
			print name

	def add(self,teamName):
		self.league.addTeam(Team(teamName, []))

	def rm(self,teamName):
		self.league.removeTeam(teamName)

class TeamShell(object):

	def __init__(self, team):
		self.team = team

	def run(self):
		while(True):
			system("clear")
			self.printRoster()
			cmd = getInput()
			if(cmd[0] == "view"):
				ps = PlayerShell(self.team.getPlayer(cmd[1]))
				ps.run()
			if(cmd[0] == "add"):
				p = Player(cmd[1], cmd[2], cmd[3], cmd[4])
				self.team.addPlayer(p)
			if(cmd[0] == "rm"):
				self.team.removePlayer(cmd[1])
			if(cmd[0] == "back"):
				break

	def printRoster(self):
		table = []
		for player in self.team.roster:
			table.append([player.fullName(), player.offense, player.defense])
		print tabulate(table,["Name","Offense","Defense"])

class PlayerShell(object):

	def __init__(self, player):
		self.player = player

	def run(self):
		while(True):
			system("clear")
			self.printPlayer()
			cmd = getInput()
			if(cmd[0] == "set"):
				self.setPlayerSkill(cmd[1], cmd[2])
			if(cmd[0] == "back"):
				break

	def printPlayer(self):
		print(("Name: %s") % (self.player.fullName()))
		print(("Offense: %d") % (self.player.offense))
		print(("Defense: %d") % (self.player.defense))

	def setPlayerSkill(self, skill, value):
		if(skill == "offense"):
			self.player.offense = int(value)
		if(skill == "defense"):
			self.player.defense = int(value)

main = init()
main.run()




