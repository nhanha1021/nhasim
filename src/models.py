import random, randomname, game

def _to_key(teamName):
		key = teamName.lower().replace(" ","")
		return key

class Player(object):
	def __init__(self, firstName, lastName, offense, defense):
		self.firstName = firstName
		self.lastName = lastName
		self.offense = int(offense)
		self.defense = int(defense)

	def get_full_name(self):
		return ("%s %s") % (self.firstName, self.lastName)

	def get_offense(self):
		return self.offense

	def set_offense(self, value):
		self.offense = value

	def get_defense(self):
		return self.defense

	def set_defense(self,value):
		self.defense = value

	def get_overall(self):
		return round((self.offense+self.defense)/2)

	@classmethod
	def random_player(cls,low,high):
		firstName = randomname.get_first_name()
		lastName = randomname.get_last_name()
		offense = random.randint(low, high)
		defense = random.randint(low, high)
		return cls(firstName, lastName, offense, defense)

class Team(object):

	def __init__(self, teamName):
		self.teamName = teamName
		self.cur_roundoster = {}

	def get_team_name(self):
		return self.teamName

	def get_player(self, playerName):
		return self.cur_roundoster[_to_key(playerName)]

	def add_player(self, player):
		self.cur_roundoster[_to_key(player.get_full_name())] = player

	def remove_player(self, playerName):
		del self.cur_roundoster[_to_key(playerName)]

	def get_all_players(self):
		return self.cur_roundoster.values()

	def avg_offense(self):
		try:
			s = sum(p.offense for p in self.get_all_players())
			return s/len(self.get_all_players())
		except(ZeroDivisionError):
			return 0

	def avg_defense(self):
		try:
			s = sum(p.defense for p in self.get_all_players())
			return s/len(self.get_all_players())
		except(ZeroDivisionError):
			return 0

class League(object):

	def __init__(self, leagueName):
		self.leagueName = leagueName
		self.teamRoster = {}
		self.draft_class = None
		self.picks_added = False

	def get_league_name(self):
		return self.leagueName

	def set_league_name(self,value):
		self.leagueName = value

	def get_team(self,teamName):
		return self.teamRoster[_to_key(teamName)]

	def get_draft_class(self):
		return self.draft_class

	def set_draft_class(self, draft_class):
		self.draft_class = draft_class

	def add_team(self, team):
		self.teamRoster[_to_key(team.teamName)] = team

	def remove_team(self, teamName):
		del self.teamRoster[_to_key(teamName)]

	def get_all_teams(self):
		return self.teamRoster.values()

	def is_picks_added(self):
		return self.picks_added

	def add_draft_picks(self):
		for pick, team_name in self.draft_class.get_draft_results():
			self.get_team(team_name).add_player(pick)
		self.picks_added = True

class DraftClass(object):

	def __init__(self, class_name):
		self.class_name = class_name
		self.results = []
		self.candidates = self._init_candidates()
		self.finished = False

	def get_class_name(self):
		return self.class_name

	def _init_candidates(self):
		candidates = {}
		count = 1
		# Top-level talent
		for i in range(random.randint(1,10)):
			candidate = Player.random_player(80,99)
			candidates[count] = candidate
			count += 1
		# Mid-level talent
		for i in range(random.randint(20,50)):
			candidate = Player.random_player(65,85)
			candidates[count] = candidate
			count += 1
		# Low-level talent
		for i in range(random.randint(30,60)):
			candidate = Player.random_player(50,75)
			candidates[count] = candidate
			count += 1

		return candidates

	def get_candidates_info(self):
		info = []
		for number, candidate in self.candidates.items():
			info.append([number, candidate.get_full_name(), candidate.offense, candidate.defense, candidate.get_overall()])
		info.sort(key=lambda x: x[0], reverse = True) 
		return info

	def draft_candidate(self, number, team_name):
		member = self.candidates.pop(number)
		self.results.append((member,team_name))
		return member

	def edit_candidate_draft_team(self, pick, team_name):
		self.results[pick] = (self.results[pick][0],team_name)

	def get_draft_results(self):
		return self.results

	def set_finished(self, value):
		self.finished = value

	def is_finished(self):
		return self.finished

class Season(object):

	def __init__(self, league, schedule, week):
		self.league = league
		self.schedule = schedule
		self.week = week
		self.results = {}
		self.standings = self._init_standings()
		self.postseason = None

	def _init_standings(self):
		standings = {}
		for team in self.league.get_all_teams():
			standings[team.get_team_name()] = [0,0]
		return standings

	def get_league(self):
		return self.league

	def get_week(self):
		return self.week

	def get_remaining_weeks(self):
		return (len(self.schedule) - self.week)

	def is_complete(self):
		if(self.get_remaining_weeks() <= 0):
			return True
		return False

	def get_week_matches(self):
		return self.schedule[self.week]

	def get_week_results(self, week):
		results = []
		for match in self.schedule[week]:
			key = match[2]
			if key in self.results:
				results.append(self.results[key])
		return results

	def get_result(self, week, game_number):
		key = (week, game_number)
		return self.results[key]

	def get_rankings(self):
		ranking = {}
		rank = 1
		for row in self.get_standings():
			team_name = row[1]
			ranking[team_name] = rank
			rank += 1
		return ranking

	def get_standings(self):
		standings = []
		for team_name,record in self.standings.items():
			standings.append([team_name, record[0], record[1]])
		standings.sort(key=lambda x: x[1],reverse=True)
		for i in range(len(standings)):
			standings[i].insert(0, i+1)
		return standings

	def set_postseason(self, postseason):
		if(self.is_complete()):
			self.postseason = postseason

	def get_postseason(self):
		return self.postseason

	def is_game_finished(self, game_number):
		if (self.week, game_number) in self.results:
			return True
		return False

	def _play_game(self, match):
		key = match[2]
		if key in self.results:
			return
		away_team = self.league.get_team(match[0])
		home_team = self.league.get_team(match[1])
		result = game.play_game(away_team, home_team)
		self.standings[result.get_winner()][0] += 1
		self.standings[result.get_loser()][1] += 1
		self.results[key] = result

	def play_specific_game(self, game_number):
		match = self.schedule[self.week][game_number]
		self._play_game(match)
		
	def advance_week(self):
		for match in self.schedule[self.week]:
			self._play_game(match)
		self.week += 1

class Postseason(object):

	def __init__(self, teams):
		self.teams = {}
		self.seeds = {}
		self.results = {}
		self.cur_round = 0
		self.complete = False
		for i in range(len(teams)):
			self.teams[teams[i].get_team_name()] = teams[i]
			self.seeds[teams[i].get_team_name()] = i+1
		self.bracket = [self._filter_bracket([team.get_team_name() for team in teams])]
		
	def _filter_bracket(self, bracket):
		filt_bracket = []
		bracket.sort(key=lambda x: self.seeds[x], reverse=False)
		start = 0
		end = len(bracket)-1
		game_number = 0
		while(start<end):
			key = (self.cur_round, game_number)
			filt_bracket.append((bracket[end],bracket[start],key))
			start += 1
			end -= 1
			game_number += 1
		return filt_bracket

	def get_cur_round(self):
		return self.cur_round

	def get_seeds(self):
		return self.seeds

	def get_result(self, rnd, game_number):
		key = (rnd,game_number)
		return self.results[key]

	def get_round_results(self, rnd):
		results = []
		for i in range(len(self.bracket[rnd])):
			key = (rnd,i)
			results.append(self.results[key])
		return results

	def get_cur_round_bracket(self):
		return self.bracket[self.cur_round]

	def get_champion(self):
		if(self.is_complete):
			key = (self.cur_round-1,0)
			return self.results[key].get_winner()
		return None

	def is_complete(self):
		return self.complete

	def _play_game(self,match):
		key = match[2]
		if key in self.results:
			return
		away_team = self.teams[match[0]]
		home_team = self.teams[match[1]]
		result = game.play_game(away_team, home_team)
		self.results[key] = result
		return result

	def play_specific_game(self, game_number):
		match = self.bracket[self.cur_round][game_number]
		self._play_game(match)

	def advance_round(self):
		cur_bracket = self.bracket[self.cur_round]
		for match in cur_bracket:
			self._play_game(match)
		next_bracket = []
		for i in range(len(self.bracket[self.cur_round])):
			key = (self.cur_round,i)
			next_bracket.append(self.results[key].get_winner())
		self.cur_round += 1
		if(len(next_bracket) == 1):
			self.complete = True
			return
		self.bracket.append(self._filter_bracket(next_bracket))




