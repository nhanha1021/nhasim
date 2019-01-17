import game, datatool, sys, schedule
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
		season = datatool.load_season(sys.argv[1])
		return SeasonShell(season)
	except(IOError):
		league = datatool.load_league(sys.argv[1])
		season_schedule = schedule.make_schedule(league.get_all_teams())
		season = Season(league, season_schedule, 0)
		return SeasonShell(season)

def _team_with_rank(team_name,rank):
	
	return ("{}_{}".format(team_name,rank))	

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
		table.append(["play X","Watch game X"])
		table.append(["play all","Play the remaining games in the week"])
		table.append(["rem","Get the number of weeks left"])
		table.append(["up","View the week's upcoming games"])
		table.append(["res X", "View the results of week X"])
		table.append(["save","Save the season"])
		table.append(["ps","Load the postseason"])
		table.append(["clear","Clear the previous commands"])
		table.append(["quit","Quit the program"])
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
			elif(cmd[0] == "play"):
				if(cmd[1] == "all"):
					self._play_all_games()
				else:
					self._play_individual_game(int(cmd[1])-1)
			elif(cmd[0] == "rem"):
				print(self.season.get_remaining_weeks())
			elif(cmd[0] == "save"):
				datatool.write_season(self.season)
				print("Saved season to disk.")
			elif(cmd[0] == "up"):
				self._print_upcoming_games()
			elif(cmd[0] == "ps"):
				self._begin_postseason()
			elif(cmd[0] == "res"):
				if(len(cmd) > 1):
					self._print_week_results(int(cmd[1])-1)
				else:
					self._print_week_results(self.season.get_week())
			elif(cmd[0] == "help"):
				self._help()
			elif(cmd[0] == "clear"):
				self._refresh()
			elif(cmd[0] == "quit"):
				break
			else:
				print("Invalid command")

	def _print_upcoming_games(self):

		def _is_big_game(at_rank, ht_rank):
			if((at_rank+ht_rank<9) and (abs(at_rank-ht_rank)<5)):
				return True
			return False

		if(self.season.get_remaining_weeks() == 0):
			print("There are no more games to be played.")
			return
		rankings = self.season.get_rankings()
		table = []
		for match in self.season.get_week_matches():
			game_number = match[2][1]+1
			at = _team_with_rank(match[0], rankings[match[0]])
			ht = _team_with_rank(match[1], rankings[match[1]])
			text = [game_number,at,"@",ht]
			if(_is_big_game(rankings[match[0]],rankings[match[1]])):
				text.append("!!!")
			table.append(text)
		print(tabulate(table))

	def _print_week_results(self, week):
		if(week > self.season.get_week()) or (week<0):
			print("Please enter a valid week.")
			return
		results = self.season.get_week_results(week)
		if(len(results)==0):
			print("No games have been played this week.")
			return
		table = []
		for result in self.season.get_week_results(week):
			at = result.get_away_team()
			ht = result.get_home_team()
			asc = result.get_away_score()
			hsc = result.get_home_score()
			table.append([at,asc,ht,hsc])
		print("Week {} Results".format(week+1))
		print(tabulate(table))

	def _advance_week(self, amount):
		if(amount > self.season.get_remaining_weeks()):
			print("Not enough weeks remaining")
			return
		for i in range(amount):
			self.season.advance_week()
		self._refresh()

	def _play_individual_game(self, game_number):
		if(game_number<0) or (game_number>len(self.season.get_week_matches())):
			print("Please enter a valid game_number")
			return
		if(self.season.is_game_finished(game_number)):
			print("Game already played.")
			return
		self.season.play_specific_game(game_number)
		result = self.season.get_result(self.season.get_week(),game_number)
		print(result.get_results())

	def _play_all_games(self):
		week = self.season.get_week()
		for i in range(len(self.season.get_week_matches())):
			if not(self.season.is_game_finished(i)):
				self.season.play_specific_game(i)
				result = self.season.get_result(week,i)
				print(result.get_results())

	def _begin_postseason(self):
		if not (self.season.is_complete()):
			print("The season is not over yet")
			return
		if(self.season.get_postseason() == None):
			team_names = [x[1] for x in self.season.get_standings()[:8]]
			teams = [self.season.get_league().get_team(team_name) for team_name in team_names]
			self.season.set_postseason(Postseason(teams))
		shell = PostseasonShell(self.season.get_postseason())
		postseason = shell.run()
		self.season.set_postseason(postseason)
		self._refresh()

class PostseasonShell(object):
	def __init__(self, postseason):
		self.postseason = postseason

	def _refresh(self):

		def _print_bracket():

			seeds = self.postseason.get_seeds()
			rnd_count = 1

			for rnd in self.postseason.get_results():
				print("Round {}".format(rnd_count))
				rnd_count += 1
				table = []
				for result in rnd:
					at = result.get_away_team()
					atr = _team_with_rank(at, seeds[at])
					ht = result.get_home_team()
					htr = _team_with_rank(ht, seeds[ht])
					asc = result.get_away_score()
					hsc = result.get_home_score()
					table.append([atr,asc,htr,hsc])
				print(tabulate(table))
				print("")

			if(self.postseason.is_complete()):
				print("Champion: {}".format(self.postseason.get_champion()))
				return

			print("Round {}".format(rnd_count))
			cur_round_bracket = self.postseason.get_cur_round_bracket()
			table = []
			for matchup in cur_round_bracket:
				at = matchup[0]
				at = _team_with_rank(at, seeds[at])
				ht = matchup[1]
				ht = _team_with_rank(ht, seeds[ht])
				table.append([at,"@",ht])
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
			elif(cmd[0] == "help"):
				self._help()
			elif(cmd[0] == "back"):
				return self.postseason
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
