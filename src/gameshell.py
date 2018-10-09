import rostertool, sys
from models import League
from game import Game
from os import system
from tabulate import tabulate

def getInput():
	inp = raw_input("\n")
	inp = inp.rstrip().lstrip()
	cmd = inp.split()
	if(len(cmd) == 0):
		return [" "]
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
		table.append(["play X Y", "Play a game between team X and Y"])
		print tabulate(table)

	def run(self):
		while(True):
			self.refresh()
			cmd = getInput()
			try:
				if(cmd[0] == "help"):
					self.help()
					self.doRefresh = False
				elif(cmd[0] == "quit"):
					break
				elif(cmd[0] == "play"):
					self.play(cmd[1], cmd[2])
					self.doRefresh = False
				else:
					print("Invalid command")
					self.doRefresh = False
			except IndexError:
				print("Error parsing command")
				self.doRefresh = False

	def printTeams(self):
		table = []
		for team in self.league.allTeams():
			table.append([team.teamName])
		print tabulate(table,["Teams"])

	def play(self,atname, htname):
		try:
			at = self.league.getTeam(atname)
			ht = self.league.getTeam(htname)
			g = Game(at, ht)
			g.playGame()
		except KeyError:
			print("Error parsing team names")
			self.doRefresh = False

main = init()
main.run()
