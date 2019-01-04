class Player(object):

	def __init__(self, firstName, lastName, offense, defense):
		self.firstName = firstName
		self.lastName = lastName
		self.offense = int(offense)
		self.defense = int(defense)

	def fullName(self):
		return ("%s %s") % (self.firstName, self.lastName)

class Team(object):

	def __init__(self, teamName):
		self.teamName = teamName
		self.roster = {}

	def getPlayer(self, playerName):
		return self.roster[self.toKey(playerName)]

	def addPlayer(self, player):
		self.roster[self.toKey(player.fullName())] = player

	def removePlayer(self, playerName):
		del self.roster[self.toKey(playerName)]

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

	def toKey(self, playerName):
		key = playerName.lower().replace(" ","")
		return key

class League(object):

	def __init__(self, leagueName):
		self.leagueName = leagueName
		self.teamRoster = {}

	def getTeam(self,teamName):
		return self.teamRoster[self.toKey(teamName)]

	def addTeam(self, team):
		self.teamRoster[self.toKey(team.teamName)] = team

	def removeTeam(self, teamName):
		del self.teamRoster[self.toKey(teamName)]

	def allTeams(self):
		return self.teamRoster.values()

	def toKey(self,teamName):
		key = teamName.lower().replace(" ","")
		return key