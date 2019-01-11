import game, rostertool
from os import system
from tabulate import tabulate


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

class Season(object):

	def __init__(self, league, schedule, week):
		self.league = league
		self.schedule = schedule
		self.week = week
		self.finished_games = []
		self.standings = {}
		self._init_standings()

	def get_week(self):
		return self.week

	def get_remaining_weeks(self):
		return (len(self.schedule) - self.week)

	def _init_standings(self):
		for team in self.league.get_all_teams():
			self.standings[team.get_team_name()] = [0,0]

	def get_standings(self):
		return self.standings

	def set_standings(self,value):
		self.standings = value

	def advance_week(self):
		if(self.get_remaining_weeks() <= 0):
			return
		for match in self.schedule[self.week]:
			away_team = self.league.get_team(match[0])
			home_team = self.league.get_team(match[1])
			result = game.play_game(away_team, home_team)
			self.standings[result.get_winner().get_team_name()][0] += 1
			self.standings[result.get_loser().get_team_name()][1] += 1
		self.week += 1

class SeasonShell(object):

	def __init__(self, season):
		self.season = season

	def _refresh(self):

		def print_standings(standings):
			table = []
			for team_name,record in standings.items():
				table.append([team_name, record[0], record[1]])
			table.sort(key=lambda x: x[1],reverse=True)
			if(self.season.get_remaining_weeks() > 0):
				print("Week {}\n".format(self.season.get_week()+1))
			else:
				print("End of Regular Season\n")
			print(tabulate(table,["Team","W","L"]))
		
		system("clear")
		print_standings(self.season.get_standings())

	def run(self):
		self._refresh()
		while(True):
			cmd = _get_input()
			if(cmd[0] == "advweek"):
				self._advance_week(int(cmd[1]))
			elif(cmd[0] == "quit"):
				break
			else:
				print("Invalid command")

	def _advance_week(self, amount):
		if(amount > self.season.get_remaining_weeks()):
			print("Not enough weeks remaining")
			return
		for i in range(amount):
			self.season.advance_week()
		self._refresh()





