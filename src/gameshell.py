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

class MainShell(object):
	def __init__(self, league):
		self.league = league

	def refresh(self):
		system("clear")
		print("League: %s\n" % self.league.leagueName)
		self.printTeams()

	def help(self):
		table = []
		table.append(["quit", "Quit the program"])
		table.append(["play X Y", "Play a game between team X and Y"])
		print tabulate(table)

	def run(self):
		self.refresh()
		while(True):
			cmd = getInput()
			try:
				if(cmd[0] == "help"):
					self.help()
				elif(cmd[0] == "quit"):
					break
				elif(cmd[0] == "play"):
					self.play(cmd[1], cmd[2])
				elif(cmd[0] == "series"):
					self.series(cmd[1], cmd[2], int(cmd[3]))
				elif(cmd[0] == "clear" or cmd[0] == "back"):
					self.refresh()
				else:
					print("Invalid command")
			except IndexError:
				print("Error parsing command")

	def printTeams(self):
		table = []
		for team in self.league.allTeams():
			table.append([team.teamName, team.avgOff(), team.avgDef()])
		print tabulate(table,["Teams", "OFF", "DEF"])

	def play(self,atname, htname):
		try:
			at = self.league.getTeam(atname)
			ht = self.league.getTeam(htname)
		except KeyError:
			print("Error parsing team names")
			self.doRefresh = False
			return
		g = Game(at, ht)
		gr = g.playGame()
		system("clear")
		print("%s: %d %s: %d\n")%(gr.atname, gr.atscore, gr.htname, gr.htscore)
		print gr.atname
		print tabulate(eventfilter(gr.atevents),["Player","Points"])+"\n"
		print gr.htname
		print tabulate(eventfilter(gr.htevents),["Player","Points"])

	def series(self, atname, htname, n):
		try:
			at = self.league.getTeam(atname)
			ht = self.league.getTeam(htname)
		except KeyError:
			print("Error parsing team names")
			self.doRefresh = False
			return
		system("clear")
		gr_table = []
		for i in range(n):
			g = Game(at, ht)
			gr_table.append(g.playGame())
		for gr in gr_table:
			print("%s: %d %s: %d")%(gr.atname, gr.atscore, gr.htname, gr.htscore)


main = init()
main.run()
