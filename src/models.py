import random, randomname

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
		firstName = randomname.getFirstName()
		lastName = randomname.getLastName()
		offense = random.randint(low, high)
		defense = random.randint(low, high)
		return cls(firstName, lastName, offense, defense)

class Team(object):

	def __init__(self, teamName):
		self.teamName = teamName
		self.roster = {}

	def getPlayer(self, playerName):
		return self.roster[_to_key(playerName)]

	def add_player(self, player):
		self.roster[_to_key(player.get_full_name())] = player

	def removePlayer(self, playerName):
		del self.roster[_to_key(playerName)]

	def allPlayers(self):
		return self.roster.values()

	def avgOff(self):
		try:
			s = sum(p.offense for p in self.allPlayers())
			return s/len(self.allPlayers())
		except(ZeroDivisionError):
			return 0

	def avgDef(self):
		try:
			s = sum(p.defense for p in self.allPlayers())
			return s/len(self.allPlayers())
		except(ZeroDivisionError):
			return 0

class League(object):

	def __init__(self, leagueName):
		self.leagueName = leagueName
		self.teamRoster = {}

	def getTeam(self,teamName):
		return self.teamRoster[_to_key(teamName)]

	def addTeam(self, team):
		self.teamRoster[_to_key(team.teamName)] = team

	def removeTeam(self, teamName):
		del self.teamRoster[_to_key(teamName)]

	def allTeams(self):
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



