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
		season_schedule = schedule.make_schedule([team.get_team_name() for team in league.get_all_teams()])
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
		table.append(["wres X", "View the results of week X"])
		table.append(["gres X Y","View the results of week X, game Y"])
		table.append(["save","Save the season"])
		table.append(["ps","Load the postseason"])
		table.append(["clear","Clear the previous commands"])
		table.append(["quit","Quit the program"])
		print(tabulate(table))

	def run(self):
		self._refresh()
		while(True):
			cmd = _get_input()
			try:
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
				elif(cmd[0] == "wres"):
					if(len(cmd) > 1):
						self._print_week_results(int(cmd[1])-1)
					else:
						self._print_week_results(self.season.get_week())
				elif(cmd[0] == "gres"):
					self._print_game_result(int(cmd[1])-1,int(cmd[2])-1)
				elif(cmd[0] == "sched"):
					self._print_team_games(cmd[1])
				elif(cmd[0] == "help"):
					self._help()
				elif(cmd[0] == "clear"):
					self._refresh()
				elif(cmd[0] == "quit"):
					break
				else:
					print("Invalid command")
			except(IndexError,ValueError):
				print("Error parsing command.")

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
		print("\nWeek {} Games".format(self.season.get_week()))
		print(tabulate(table))

	def _print_team_games(self,team_name):
		s = self.season.get_team_matches(team_name)
		team_name = self.season.get_league().get_team(team_name).get_team_name()
		table = []
		for game in s:
			week = game[2][0]
			game_num = game[2][1]
			if(self.season.is_game_finished(week,game_num)):
				result = self.season.get_result(week,game_num)
				if(result.get_winner() == team_name):
					r = "W"
				else:
					r = "L"
				at = result.get_away_team()
				ht = result.get_home_team()
				asc = result.get_away_score()
				hsc = result.get_home_score()
				table.append([week+1,at,asc,ht,hsc,r])
			else:
				table.append([week+1,game[0],"@",game[1]])
		print("\n{}'s Schedule".format(team_name))
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
		for result, game_number in results:
			at = result.get_away_team()
			ht = result.get_home_team()
			asc = result.get_away_score()
			hsc = result.get_home_score()
			table.append([game_number+1,at,asc,ht,hsc])
		print("\nWeek {} Results".format(week+1))
		print(tabulate(table))

	def _print_game_result(self, week, game_number):
		if not(self.season.is_game_finished(week,game_number)):
			print("This game has not been completed yet.")
			return
		result = self.season.get_result(week, game_number)
		print("\nWeek {}, Game {} Result".format(week+1, game_number+1))
		print(result.get_results())

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
		week = self.season.get_week()
		self.season.play_specific_game(week,game_number)
		result = self.season.get_result(week,game_number)
		print("\n"+result.get_results())

	def _play_all_games(self):
		print("")
		week = self.season.get_week()
		for i in range(len(self.season.get_week_matches())):
			if not(self.season.is_game_finished(week,i)):
				self.season.play_specific_game(week,i)
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

		def print_results():
			seeds = self.postseason.get_seeds()
			for rnd in range(self.postseason.get_cur_round()):
				results = self.postseason.get_round_results(rnd)
				table = []
				for result, game_number in results:
					text = []
					at = result.get_away_team()
					at = _team_with_rank(at,seeds[at])
					ht = result.get_home_team()
					ht = _team_with_rank(ht,seeds[ht])
					asc = result.get_away_score()
					hsc = result.get_home_score()
					table.append([game_number+1,at,asc,ht,hsc])
				print("Round {}".format(rnd+1))
				print(tabulate(table))
				print("")
			if(self.postseason.is_complete()):
				print("Champion: {}".format(self.postseason.get_champion()))

		def print_bracket():
			seeds = self.postseason.get_seeds()
			table = []
			for match in self.postseason.get_cur_round_bracket():
				at = _team_with_rank(match[0],seeds[match[0]])
				ht = _team_with_rank(match[1],seeds[match[1]])
				game_number = match[2][1]+1
				table.append([game_number,at,"@",ht])
			print("Round {}".format(self.postseason.get_cur_round()+1))
			print(tabulate(table))

		system("clear")
		print_results()
		if not(self.postseason.is_complete()):
			print_bracket()

	def _help(self):
		table = []
		table.append(["adv","Advance to the next round"])
		table.append(["play X", "Play game x in the current round"])
		table.append(["gres X Y", "View the results of round X, game Y"])
		table.append(["clear","Clear the previous commands"])
		table.append(["back","Return to the previous screen"])
		print(tabulate(table))

	def run(self):
		self._refresh()
		while(True):
			cmd = _get_input()
			try:
				if(cmd[0] == "adv"):
					self._advance_round()
				elif(cmd[0] == "play"):
					self._play_individual_game(int(cmd[1])-1)
				elif(cmd[0] == "gres"):
					self._print_game_result(int(cmd[1])-1,int(cmd[2])-1)
				elif(cmd[0] == "clear"):
					self._refresh()
				elif(cmd[0] == "help"):
					self._help()
				elif(cmd[0] == "back"):
					return self.postseason
				else:
					print("Invalid command")
			except(IndexError,ValueError):
				print("Error parsing command.")

	def _print_game_result(self, rnd, game_number):
		if not(self.postseason.is_game_finished(rnd,game_number)):
			print("This game has not been completed yet.")
			return
		result = self.postseason.get_result(rnd, game_number)
		print("\nRound {}, Game {} Result".format(rnd+1, game_number+1))
		print(result.get_results())


	def _play_individual_game(self, game_number):
		if(game_number<0) or (game_number>=len(self.postseason.get_cur_round_bracket())):
			print("Please enter a valid game number.")
			return
		self.postseason.play_specific_game(game_number)
		result = self.postseason.get_result(self.postseason.get_cur_round(),game_number)
		print(result.get_results())

	def _advance_round(self):
		if(self.postseason.is_complete()):
			print("Postseason is complete.")
			return
		self.postseason.advance_round() 
		self._refresh()

shell = _initialize()
shell.run()
