class Player(object):

	def __init__(self, firstName, lastName, offense, defense):
		self.firstName = firstName
		self.lastName = lastName
		self.offense = offense
		self.defense = defense

	def fullName(self):
		return ("%s %s") % (self.firstName, self.lastName)

class Team(object):

	def __init__(self, teamName, roster):
		self.teamName = teamName
		self.roster = roster

	def getPlayer(self, playerName):
		for player in self.roster:
			if(player.fullName() == playerName):
				return player

	def addPlayer(self, player):
		self.roster.append(player)

	def removePlayer(self, playerName):
		for i in range(len(self.roster)):
			if(self.roster[i].fullName() == playerName):
				del self.roster[i]
				break

class League(object):

	def __init__(self, leagueName, teamRoster):
		self.leagueName = leagueName
		self.teamRoster = teamRoster

	def getTeam(self,teamName):
		return self.teamRoster[teamName]

	def addTeam(self, team):
		self.teamRoster[team.teamName] = team

	def removeTeam(self, teamName):
		del self.teamRoster[teamName]