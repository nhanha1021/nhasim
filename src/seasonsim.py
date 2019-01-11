import game, rostertool
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

	def _help(self):
		table = []
		table.append(["advweek X","Advance X weeks ahead"])
		table.append(["remweek","Get the number of weeks left"])
		table.append(["quit","Quit the program"])
		print(tabulate(table))

	def run(self):
		self._refresh()
		while(True):
			cmd = _get_input()
			if(cmd[0] == "advweek"):
				if(len(cmd) > 1):
					self._advance_week(int(cmd[1]))
				else:
					self._advance_week(1)
			elif(cmd[0] == "remweek"):
				print(self.season.get_remaining_weeks())
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




