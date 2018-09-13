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

class League(object):

	def __init__(self, leagueName, teamRoster):
		self.leagueName = leagueName
		self.teamRoster = teamRoster

	def getTeam(self,teamName):
		return self.teamRoster[teamName]