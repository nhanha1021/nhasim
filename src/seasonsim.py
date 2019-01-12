import game, rostertool, sys, schedule
from os import system
from tabulate import tabulate
from models import Season

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

		def print_standings(standings):
			table = []
			for team_name,record in standings.items():
				table.append([team_name, record[0], record[1]])
			table.sort(key=lambda x: x[1],reverse=True)
			rank = 1
			for row in table:
				row.insert(0, rank)
				rank += 1
			if(self.season.get_remaining_weeks() > 0):
				print("Week {}\n".format(self.season.get_week()+1))
			else:
				print("End of Regular Season\n")
			print(tabulate(table,["Rank","Team","W","L"]))
		
		system("clear")
		print_standings(self.season.get_standings())

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

class PostseasonShell(object):
	def __init__(self, postseason):
		self.postseason = postseason

	def _refresh(self):
		def _print_bracket():
			rnd_count = 1
			for rnd in self.postseason.get_results():
				print("Round {}".format(rnd_count))
				rnd_count += 1
				for result in rnd:
					print result.get_results()
				print("")

			if(self.postseason.is_complete()):
				print("Champion: {}".format(self.postseason.get_champion().get_team_name()))
				return

			print("Round {}".format(rnd_count))
			cur_round_bracket = self.postseason.get_cur_round_bracket()
			start = 0
			end = len(cur_round_bracket)-1
			while(start<end):
				print("{} vs {}".format(cur_round_bracket[start].get_team_name(),cur_round_bracket[end].get_team_name()))
				start += 1
				end -= 1
		
		system("clear")
		_print_bracket()

	def run(self):
		self._refresh()
		while(True):
			cmd = _get_input()
			if(cmd[0] == "adv"):
				self._advance_round()
			elif(cmd[0] == "quit"):
				break
			else:
				print("Invalid command")

	def _advance_round(self):
		if(self.postseason.is_complete()):
			print("Postseason is complete.")
			return
		self.postseason.advance_round() 
		self._refresh()

#shell = _initialize()
#shell.run()
