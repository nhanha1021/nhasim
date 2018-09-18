import sys, rostertool
from models import League, Team, Player
from tabulate import tabulate
from os import system

def getInput():
	inp = raw_input("\n")
	inp = inp.rstrip().lstrip()
	cmd = inp.split(' ')
	for i in range(len(cmd)):
		cmd[i] = cmd[i].rstrip().lstrip()
		cmd[i] = cmd[i].replace("_", " ")
	return cmd

def init():
	system("clear")
	league = rostertool.loadLeague(sys.argv[1])
	return MainShell(league)

class MainShell(object):

	def __init__(self, league):
		self.league = league
		self.doRefresh = True

	def refresh(self):
		if(self.doRefresh):
			system("clear")
			self.printTeams()
		self.doRefresh = True

	def run(self):
		while(True):
			self.refresh()
			cmd = getInput()
			if(cmd[0] == "add"):
				self.add(cmd[1])
			if(cmd[0] == "rm"):
				self.rm(cmd[1])
			if(cmd[0] == "view"):
				ts = TeamShell(self.league.getTeam(cmd[1]))
				ts.run()
			if(cmd[0] == "help"):
				self.help()
				self.doRefresh = False
			if(cmd[0] == "quit"):
				break

	def printTeams(self):
		for name in self.league.teamRoster.keys():
			print name

	def add(self,teamName):
		self.league.addTeam(Team(teamName, []))

	def rm(self,teamName):
		self.league.removeTeam(teamName)

	def help(self):
		print("")
		print("add X - Add a team named X to the league")
		print("rm X - Remove team X from the league")
		print("view X - View the details of team X")
		print("quit - End the program")

class TeamShell(object):

	def __init__(self, team):
		self.team = team
		self.doRefresh = True

	def refresh(self):
		if(self.doRefresh):
			system("clear")
			self.printRoster()
		self.doRefresh = True

	def run(self):
		while(True):
			self.refresh()
			cmd = getInput()
			if(cmd[0] == "view"):
				ps = PlayerShell(self.team.getPlayer(cmd[1]))
				ps.run()
			if(cmd[0] == "add"):
				p = Player(cmd[1], cmd[2], cmd[3], cmd[4])
				self.team.addPlayer(p)
			if(cmd[0] == "rm"):
				self.team.removePlayer(cmd[1])
			if(cmd[0] == "help"):
				self.help()
				self.doRefresh = False
			if(cmd[0] == "back"):
				break

	def help(self):
		print("")
		print("add X Y A B - Add player with first name X, last name Y, offense A, and defense B to the team")
		print("rm X - Remove player X from the team")
		print("view X - View the details of player X")
		print("back - Return to the league screen")

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




