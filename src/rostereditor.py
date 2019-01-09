import sys, rostertool
from models import *
from tabulate import tabulate
from os import system

def _get_input():
	inp = raw_input("\n>")
	inp = inp.rstrip().lstrip()
	cmd = inp.split()
	if(len(cmd) == 0):
		return [" "]
	for i in range(len(cmd)):
		cmd[i] = cmd[i].rstrip().lstrip()
		cmd[i] = cmd[i].replace("_", " ")
	return cmd

def _initialize():
	system("clear")
	if(len(sys.argv) == 1):
		league = League("")
	else:
		league = rostertool.loadLeague(sys.argv[1])
	return MainShell(league)

class MainShell(object):
	def __init__(self, league):
		self.league = league

	def _refresh(self):
		system("clear")
		print(self.league.get_league_name()+"\n")
		self._print_teams()

	def _help(self):
		table = []
		table.append(["add X", "Add a team named X to the league"])
		table.append(["rm X", "Remove team X from the league"])
		table.append(["view X", "View the details of team X"])
		table.append(["setname X", "Set the name of the league to X"])
		table.append(["mktrade X Y", "Make a trade between Team X and Team Y"])
		table.append(["draft", "Create a draft for the league"])
		table.append(["save","Save the current league"])
		table.append(["saveas X", "Save the league under the name X"])
		table.append(["quit","End the program"])
		print(tabulate(table))

	def run(self):
		self._refresh()
		while(True):
			cmd = _get_input()
			try:
				if(cmd[0] == "add"):
					self._add_team(cmd[1])
				elif(cmd[0] == "rm"):
					self._remove_team(cmd[1])
				elif(cmd[0] == "view"):
					self._view_team(cmd[1])
				elif(cmd[0] == "setname"):
					self._set_name(cmd[1])
				elif(cmd[0] == "save"):
					self._save()
				elif(cmd[0] == "saveas"):
					self._save_as(cmd[1])
				elif(cmd[0] == "mktrade"):
					self._make_trade(cmd[1], cmd[2])
				elif(cmd[0] == "draft"):
					self._draft()
				elif(cmd[0] == "help"):
					self._help()
				elif(cmd[0] == "quit"):
					break
				else:
					print("Invalid command")
			except(IndexError):
				print("Error parsing command")

	def _print_teams(self):
		table = []
		for team in self.league.get_all_teams():
			table.append([team.get_team_name(), team.avg_offense(), team.avg_defense()])
		print tabulate(table,["Teams", "OFF", "DEF"])

	def _view_team(self,teamName):
		try:
			team = self.league.get_team(teamName)
			ts = TeamShell(team)
			ts.run()
			self._refresh()
		except(KeyError):
			print("Error parsing team name")

	def _add_team(self,teamName):
		self.league.add_team(Team(teamName))

	def _remove_team(self,teamName):
		try:
			self.league.remove_team(teamName)
			self._refresh()
		except(KeyError):
			print("Error parsing team name")

	def _set_name(self, name):
		self.league.set_league_name(name)
		self._refresh()

	def _save(self):
		rostertool.writeLeague(self.league)

	def _save_as(self, name):
		self.league.set_league_name(name)
		rostertool.writeLeague(self.league)

	def _make_trade(self, team1Name, team2Name):
		try:
			team1 = self.league.get_team(team1Name)
			team2 = self.league.get_team(team2Name)
			ts = TradeShell(team1, team2)
			ts.run()
			self._refresh()
		except(KeyError):
			print("Error parsing team names")

	def _draft(self):
		draft_name = self.league.get_league_name()+"Draft Class"
		draft_class = DraftClass(draft_name)
		draft_shell = DraftShell(self.league, draft_class)
		draft_shell.run()
		self._refresh()

class TeamShell(object):
	def __init__(self, team):
		self.team = team

	def _refresh(self):
		system("clear")
		self._print_roster()

	def _help(self):
		table = []
		table.append(["add", "Add player to the team"])
		table.append(["addrand X", "Add a random player to the team of grade A,B,C"])
		table.append(["rm X", "Remove player X from the team"])
		table.append(["view X","View the details of player X"])
		table.append(["back","Return to the league screen"])
		print tabulate(table)

	def run(self):
		self._refresh()
		while(True):
			cmd = _get_input()
			try:
				if(cmd[0] == "view"):
					self._view(cmd[1])
				elif(cmd[0] == "add"):
					self._add_player()
				elif(cmd[0] == "addrand"):
					self._add_random_player(cmd[1])
				elif(cmd[0] == "rm"):
					self._remove_player(cmd[1])
				elif(cmd[0] == "help"):
					self._help()
				elif(cmd[0] == "back"):
					break
				else:
					print("Invalid command")
			except(IndexError):
				print("Error parsing command")

	def _print_roster(self):
		table = []
		for player in self.team.get_all_players():
			table.append([player.get_full_name(), player.get_offense(), player.get_defense()])
		print(self.team.get_team_name()+"\n")	
		print(tabulate(table,["Name","Offense","Defense"]))

	def _view(self, playerName):
		try:
			player = self.team.get_player(playerName)
			ps = PlayerShell(player)
			ps.run()
			self._refresh()
		except(KeyError):
			print("Error parsing player name")

	def _add_player(self):
		first = raw_input("First Name: ")
		last = raw_input("Last Name: ")
		off = raw_input("Offense: ")
		defs = raw_input("Defense: ")
		self.team.add_player(Player(first,last,off,defs))
		self._refresh()

	def _add_random_player(self, grade):
		if(grade=="A"):
			self.team.add_player(Player.random_player(85,99))
		if(grade=="B"):
			self.team.add_player(Player.random_player(75,89))
		if(grade=="C"):
			self.team.add_player(Player.random_player(55,75))
		self._refresh()

	def _remove_player(self, player_name):
		try:
			self.team.remove_player(player_name)
			self._refresh()
		except(KeyError):
			print("Error parsing player name")

class PlayerShell(object):
	def __init__(self, player):
		self.player = player

	def _refresh(self):
		system("clear")
		self._print_player()

	def _help(self):
		table = []
		table.append(["set off X","Set the get_offense() of the current player to X"])
		table.append(["set def X", "Set the get_defense() of the current player to X"])
		table.append(["back","Return to the previous screen"])
		print(tabulate(table))

	def run(self):
		self._refresh()
		while(True):
			cmd = _get_input()
			try:
				if(cmd[0] == "set"):
					self._set(cmd[1], cmd[2])
				elif(cmd[0] == "help"):
					self._help()
				elif(cmd[0] == "back"):
					break
				else:
					print("Invalid command")
			except IndexError:
				print("Error parsing command")

	def _print_player(self):
		print(self.player.get_full_name()+"\n")
		print(("Offense: %d") % (self.player.get_offense()))
		print(("Defense: %d") % (self.player.get_defense()))

	def _set(self, item, value):
		if(item == "off"):
			self.player.set_offense(int(value))
		elif(item == "def"):
			self.player.set_defense(int(value))
		else:
			print("Error parsing command")
			return
		self._refresh()

class TradeShell(object):
	def __init__(self, team1, team2):
		self.team1 = team1
		self.team2 = team2
		self.doRefresh = True

	def _refresh(self):
		system("clear")
		self._print_rosters()

	def _help(self):
		table = []
		table.append(["trade X Y","Trade Player X from Team 1 to Team 2 \nand Player Y from Team 2 to Team 1. \nType '*' in place of a blank player \nType ',' to separate multiple players"])
		table.append(["back","Return to the previous screen"])
		print tabulate(table)

	def run(self):
		self._refresh()
		while(True):
			cmd = _get_input()
			try:
				if(cmd[0] == "trade"):
					self._trade(cmd[1],cmd[2])
				elif(cmd[0] == "help"):
					self._help()
				elif(cmd[0] == "back"):
					break
				else:
					print("Invalid command")
			except IndexError:
				print("Error parsing command")

	def _print_rosters(self):
		table1 = []
		for player in self.team1.get_all_players():
			table1.append([player.get_full_name(),player.get_offense(),player.get_defense()])
		table2 = []
		for player in self.team2.get_all_players():
			table2.append([player.get_full_name(),player.get_offense(),player.get_defense()])
		print self.team1.get_team_name()
		print tabulate(table1,["Name","Offense","Defense"])
		print ""
		print self.team2.get_team_name()
		print tabulate(table2,["Name","Offense","Defense"])

	def _trade(self,team1Names, team2Names):
		try:
			players1 = []
			players2 = []
			if((team1Names == "*") != True):
				names1 = team1Names.split(",")
				for name in names1:
					players1.append(self.team1.get_player(name))
			if((team2Names == "*") != True):
				names2 = team2Names.split(",")
				for name in names2:
					players2.append(self.team2.get_player(name))
		except KeyError:
			print("Error parsing player names")
			return
		for player in players1:
			self.team1.remove_player(player.get_full_name())
			self.team2.add_player(player)
		for player in players2:
			self.team2.remove_player(player.get_full_name())
			self.team1.add_player(player)
		self._refresh()

class DraftShell(object):
	def __init__(self, league, draft_class):
		self.league = league
		self.draft_class = draft_class

	def _help(self):
		table = []
		table.append(["cand","View the remaining draft candidates"])
		table.append(["draft X Y","Draft candidate with number X to team Y"])
		table.append(["back","Quit the draft without saving"])
		table.append(["finish","Finish the draft and exit"])
		print(tabulate(table))

	def _refresh(self):
		system("clear")
		self._print_draft_results()

	def run(self):
		system("clear")
		print("Welcome to the {} Draft!".format(self.league.get_league_name()))
		while(True):
			cmd = _get_input()
			try:
				if(cmd[0] == "back"):
					break
				elif(cmd[0] == "help"):
					self._help()
				elif(cmd[0] == "cand"):
					self._print_candidates()
				elif(cmd[0] == "draft"):
					self._draft_player(int(cmd[1]),cmd[2])
				elif(cmd[0] == "finish"):
					self._finish_draft()
					break
				else:
					print("Invalid Command")
			except(IndexError, ValueError):
				print("Error parsing command")

	def _print_draft_results(self):
		results = []
		count = 1
		for member, team_name in self.draft_class.get_draft_results():
			results.append([count,member.get_full_name(),team_name])
			count += 1
		print("Draft Results\n")
		print(tabulate(results,["Pick","Player","Drafted By"]))

	def _print_candidates(self):
		table = self.draft_class.get_candidates_info()
		print("\n"+tabulate(table,["ID","Name","Offense","Defense"]))

	def _draft_player(self, number, team_name):
		try:
			drafting_team_name = self.league.get_team(team_name).get_team_name()
		except(KeyError):
			print("Error parsing team name")
		try:
			player = self.draft_class.draft_candidate(number, drafting_team_name)
			self._refresh()
		except(KeyError):
			print("Error parsing draft number")

	def _finish_draft(self):
		for member, team_name in self.draft_class.get_draft_results():
			self.league.get_team(team_name).add_player(member)
			
main = _initialize()
main.run()




