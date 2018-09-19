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
	if(len(sys.argv) == 1):
		league = League("")
	else:
		league = rostertool.loadLeague(sys.argv[1])
	return MainShell(league)

class MainShell(object):

	def __init__(self, league):
		self.league = league
		self.doRefresh = True

	def refresh(self):
		if(self.doRefresh):
			system("clear")
			print("League: %s\n" % self.league.leagueName)
			self.printTeams()
		self.doRefresh = True

	def help(self):
		table = []
		table.append(["add X", "Add a team named X to the league"])
		table.append(["rm X", "Remove team X from the league"])
		table.append(["view X", "View the details of team X"])
		table.append(["set name X", "Set the name of the leauge to X"])
		table.append(["quit","End the program"])
		print tabulate(table)

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
			if(cmd[0] == "set"):
				self.set(cmd[1], cmd[2])
			if(cmd[0] == "save"):
				self.save()
			if(cmd[0] == "help"):
				self.help()
				self.doRefresh = False
			if(cmd[0] == "quit"):
				break

	def printTeams(self):
		table = []
		for name in self.league.teamRoster.keys():
			table.append([name])
		print tabulate(table,["Teams"])

	def add(self,teamName):
		self.league.addTeam(Team(teamName, []))

	def rm(self,teamName):
		self.league.removeTeam(teamName)

	def set(self,item,value):
		if(item == "name"):
			self.league.leagueName = value

	def save(self):
		rostertool.writeLeague(self.league)

class TeamShell(object):

	def __init__(self, team):
		self.team = team
		self.doRefresh = True

	def refresh(self):
		if(self.doRefresh):
			system("clear")
			self.printRoster()
		self.doRefresh = True

	def help(self):
		table = []
		table.append(["add", "Add player to the team"])
		table.append(["addrand", "Add a random player to the team"])
		table.append(["rm X", "Remove player X from the team"])
		table.append(["view X","View the details of player X"])
		table.append(["back","Return to the league screen"])
		print tabulate(table)

	def run(self):
		while(True):
			self.refresh()
			cmd = getInput()
			if(cmd[0] == "view"):
				ps = PlayerShell(self.team.getPlayer(cmd[1]))
				ps.run()
			if(cmd[0] == "add"):
				self.add()
			if(cmd[0] == "addrand"):
				self.addrand()
			if(cmd[0] == "rm"):
				self.team.removePlayer(cmd[1])
			if(cmd[0] == "help"):
				self.help()
				self.doRefresh = False
			if(cmd[0] == "back"):
				break

	def printRoster(self):
		table = []
		for player in self.team.roster:
			table.append([player.fullName(), player.offense, player.defense])
		print tabulate(table,["Name","Offense","Defense"])

	def add(self):
		first = raw_input("First Name: ")
		last = raw_input("Last Name: ")
		off = raw_input("Offense: ")
		defs = raw_input("Defense: ")
		self.team.addPlayer(Player(first,last,off,defs))

	def addrand(self):
		self.team.addPlayer(rostertool.createRandomPlayer(50,99))

class PlayerShell(object):

	def __init__(self, player):
		self.player = player
		self.doRefresh = True

	def refresh(self):
		if(self.doRefresh):
			system("clear")
			self.printPlayer()
		self.doRefresh = True

	def help(self):
		table = []
		table.append(["set off X","Set the offense of the current player to X"])
		table.append(["set def X", "Set the defense of the current player to X"])
		table.append(["set name X","Set the name of the current player to X"])
		table.append(["back","Return to the previous screen"])
		print tabulate(table)

	def run(self):
		while(True):
			self.refresh()
			cmd = getInput()
			if(cmd[0] == "set"):
				self.set(cmd[1], cmd[2])
			if(cmd[0] == "help"):
				self.help()
				self.doRefresh = False
			if(cmd[0] == "back"):
				break

	def printPlayer(self):
		print(("Name: %s") % (self.player.fullName()))
		print(("Offense: %d") % (self.player.offense))
		print(("Defense: %d") % (self.player.defense))

	def set(self, item, value):
		if(item == "off"):
			self.player.offense = int(value)
		if(item == "def"):
			self.player.defense = int(value)
		if(item == "name"):
			value = value.split(" ")
			self.player.firstName = value[0]
			self.player.lastName = value[1]

main = init()
main.run()




