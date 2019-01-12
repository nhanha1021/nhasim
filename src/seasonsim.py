import game, rostertool, sys, schedule
from os import system
from tabulate import tabulate
from models import Season, Postseason

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
	try:
		system("clear")
		season = rostertool.load_season(sys.argv[1])
		return SeasonShell(season)
	except(IOError):
		league = rostertool.load_league(sys.argv[1])
		season_schedule = schedule.make_schedule(league.get_all_teams())
		season = Season(league, season_schedule, 0)
		return SeasonShell(season)

class SeasonShell(object):

	def __init__(self, season):
		self.season = season

	def _refresh(self):

		def print_standings():
			table = self.season.get_standings()
			if(self.season.is_complete()):
				print("End of Regular Season\n")
			else:
				print("Week {}\n".format(self.season.get_week()+1))		
			print(tabulate(table,["Rank","Team","W","L"]))
		
		system("clear")
		print_standings()

	def _help(self):
		table = []
		table.append(["adv X","Advance X weeks ahead"])
		table.append(["rem","Get the number of weeks left"])
		table.append(["quit","Quit the program"])
		table.append(["save","Save the season"])
		print(tabulate(table))

	def run(self):
		self._refresh()
		while(True):
			cmd = _get_input()
			if(cmd[0] == "adv"):
				if(len(cmd) > 1):
					self._advance_week(int(cmd[1]))
				else:
					self._advance_week(1)
			elif(cmd[0] == "rem"):
				print(self.season.get_remaining_weeks())
			elif(cmd[0] == "save"):
				rostertool.write_season(self.season)
				print("Saved season to disk.")
			elif(cmd[0] == "postseason"):
				self._begin_postseason()
			elif(cmd[0] == "help"):
				self._help()
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

	def _begin_postseason(self):
		if not (self.season.is_complete()):
			print("The season is not over yet")
			return
		teams = self.season.get_postseason_teams()
		postseason = Postseason(teams)
		shell = PostseasonShell(postseason)
		shell.run()
		self._refresh()

class PostseasonShell(object):
	def __init__(self, postseason):
		self.postseason = postseason

	def _refresh(self):

		def _print_bracket():
			rnd_count = 1
			for rnd in self.postseason.get_results():
				print("Round {}".format(rnd_count))
				rnd_count += 1
				table = []
				for result in rnd:
					away_team = result.get_away_team().get_team_name()
					home_team = result.get_home_team().get_team_name()
					table.append(["{}_{}".format(away_team, self.postseason.get_seed(away_team)), result.get_away_score(), "{}_{}".format(home_team, self.postseason.get_seed(home_team)), result.get_home_score()])
				print(tabulate(table))
				print("")

			if(self.postseason.is_complete()):
				print("Champion: {}".format(self.postseason.get_champion().get_team_name()))
				return

			print("Round {}".format(rnd_count))
			cur_round_bracket = self.postseason.get_cur_round_bracket()
			table = []
			for matchup in cur_round_bracket:
				away_team = matchup[0].get_team_name()
				home_team = matchup[1].get_team_name()
				table.append(["{}_{}".format(away_team,self.postseason.get_seed(away_team)),"@","{}_{}".format(home_team,self.postseason.get_seed(home_team))])
			print(tabulate(table))
		
		system("clear")
		_print_bracket()

	def _help(self):
		table = []
		table.append(["adv","Advance to the next round"])
		table.append(["back","Return to the previous screen"])

	def run(self):
		self._refresh()
		while(True):
			cmd = _get_input()
			if(cmd[0] == "adv"):
				self._advance_round()
			elif(cmd[0] == "back"):
				break
			else:
				print("Invalid command")

	def _advance_round(self):
		if(self.postseason.is_complete()):
			print("Postseason is complete.")
			return
		self.postseason.advance_round() 
		self._refresh()

shell = _initialize()
shell.run()
