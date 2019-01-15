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

	@classmethod
	def random_player(cls,low,high):
		firstName = randomname.get_first_name()()
		lastName = randomname.get_last_name()
		offense = random.cur_roundandint(low, high)
		defense = random.cur_roundandint(low, high)
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

	def get_league_name(self):
		return self.leagueName

	def set_league_name(self,value):
		self.leagueName = value

	def get_team(self,teamName):
		return self.teamRoster[_to_key(teamName)]

	def add_team(self, team):
		self.teamRoster[_to_key(team.teamName)] = team

	def remove_team(self, teamName):
		del self.teamRoster[_to_key(teamName)]

	def get_all_teams(self):
		return self.teamRoster.values()

class DraftClass(object):

	def __init__(self, class_name):
		self.class_name = class_name
		self.members = []
		self.candidates = self._init_candidates()

	def get_class_name(self):
		return self.class_name

	def _init_candidates(self):
		candidates = {}
		count = 0
		# Top-level talent
		for i in range(random.cur_roundandint(1,10)):
			candidate = Player.cur_roundandom_player(80,99)
			candidates[count] = candidate
			count += 1
		# Mid-level talent
		for i in range(random.cur_roundandint(20,50)):
			candidate = Player.cur_roundandom_player(65,85)
			candidates[count] = candidate
			count += 1
		# Low-level talent
		for i in range(random.cur_roundandint(30,60)):
			candidate = Player.cur_roundandom_player(50,75)
			candidates[count] = candidate
			count += 1

		return candidates

	def get_candidates_info(self):
		info = []
		for number, candidate in self.candidates.items():
			info.append([number, candidate.get_full_name(), candidate.offense, candidate.defense]) 
		return info

	def draft_candidate(self, number, team_name):
		member = self.candidates.pop(number)
		self.members.append((member,team_name))
		return member

	def get_draft_results(self):
		return self.members

class Season(object):

	def __init__(self, league, schedule, week):
		self.league = league
		self.schedule = schedule
		self.week = week
		self.results = []
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

	def get_last_week_results(self):
		return self.results[self.week-1]

	def get_rankings(self):
		ranking = {}
		rank = 1
		for row in self.get_standings():
			team_name = row[1]
			ranking[team_name] = rank
			rank += 1
		return ranking

	def get_standings(self):
		table = []
		for team_name,record in self.standings.items():
			table.append([team_name, record[0], record[1]])
		table.sort(key=lambda x: x[1],reverse=True)
		rank = 1
		for row in table:
			row.insert(0, rank)
			rank += 1
		return table

	def get_postseason_teams(self):
		top_eight = [x[1] for x in self.get_standings()[:8]]
		return top_eight

	def set_postseason(self, postseason):
		if(self.is_complete()):
			self.postseason = postseason

	def get_postseason(self):
		return self.postseason

	def advance_week(self):
		week_results = []
		for match in self.schedule[self.week]:
			away_team = self.league.get_team(match[0])
			home_team = self.league.get_team(match[1])
			result = game.play_game(away_team, home_team)
			self.standings[result.get_winner()][0] += 1
			self.standings[result.get_loser()][1] += 1
			week_results.append(result)
		self.results.append(week_results)
		self.week += 1

class Postseason(object):

	def __init__(self, team_names, league):
		self.league = league
		self.seeds = {}
		for i in range(len(team_names)):
			self.seeds[team_names[i]] = i+1
		self.bracket = [self._filter_bracket(team_names)]
		self.results = []
		self.cur_round = 0
		self.complete = False

	def _filter_bracket(self, bracket):
		filt_bracket = []
		bracket.sort(key=lambda x: self.seeds[x], reverse=False)
		start = 0
		end = len(bracket)-1
		while(start<end):
			filt_bracket.append((bracket[end],bracket[start]))
			start += 1
			end -= 1
		return filt_bracket

	def get_seeds(self):
		return self.seeds

	def get_results(self):
		return self.results

	def get_cur_round_bracket(self):
		return self.bracket[self.cur_round]

	def get_champion(self):
		if(self.is_complete):
			return self.results[self.cur_round][0].get_winner()
		return None

	def is_complete(self):
		return self.complete

	def advance_round(self):
		next_bracket = []
		round_results = []
		cur_bracket = self.bracket[self.cur_round]
		for matchup in cur_bracket:
			away_team = self.league.get_team(matchup[0])
			home_team = self.league.get_team(matchup[1])
			result = game.play_game(away_team, home_team)
			round_results.append(result)
			next_bracket.append(result.get_winner())
		self.results.append(round_results)
		if(len(next_bracket) == 1):
			self.complete = True
			return
		self.bracket.append(self._filter_bracket(next_bracket))
		self.cur_round += 1









