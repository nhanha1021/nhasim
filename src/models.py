class Player(object):

	def __init__(self, firstName, lastName):
		self.firstName = firstName
		self.lastName = lastName

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

