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
		offense = random.randint(low, high)
		defense = random.randint(low, high)
		return cls(firstName, lastName, offense, defense)

class Team(object):

	def __init__(self, teamName):
		self.teamName = teamName
		self.roster = {}

	def get_team_name(self):
		return self.teamName

	def get_player(self, playerName):
		return self.roster[_to_key(playerName)]

	def add_player(self, player):
		self.roster[_to_key(player.get_full_name())] = player

	def remove_player(self, playerName):
		del self.roster[_to_key(playerName)]

	def get_all_players(self):
		return self.roster.values()

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



