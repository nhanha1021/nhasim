import random

class Game(object):

	def __init__(self, awayTeam, homeTeam):
		self.awayTeam = awayTeam
		self.homeTeam = homeTeam
		self.awayScore = 0
		self.homeScore = 0
		self.awayEvents = []
		self.homeEvents = []

	def play_game(self):
		self.play(3)
		while(self.awayScore == self.homeScore):
			self.play(1)
		return GameResult(self.awayTeam.teamName, self.awayScore, self.awayEvents, self.homeTeam.teamName, self.homeScore, self.homeEvents)

	def play(self, n):
		for i in range(n):
			for player in self.awayTeam.allPlayers():
				e = self.calcScore(player, self.homeTeam.allPlayers())
				self.awayEvents.append(e)
				self.awayScore += e.point
			for player in self.homeTeam.allPlayers():
				e = self.calcScore(player, self.awayTeam.allPlayers())
				self.homeEvents.append(e)
				self.homeScore += e.point

	def headline(self):
		return ("{} @ {}".format(self.awayTeam.teamName,self.homeTeam.teamName))

	def calcScore(self, player, get_defense()):
		d = random.sample(get_defense(), 3)
		dsum = sum(p.get_defense() for p in d)
		i = random.randint(0, dsum)
		if(i<player.get_offense()):
			return Event(1, player.get_full_name())
		return Event(0, player.get_full_name())

class GameResult(object):

	def __init__(self, atname, atscore, atevents, htname, htscore, htevents):
		self.atname = atname
		self.atscore = atscore
		self.atevents = atevents
		self.htname = htname
		self.htscore = htscore
		self.htevents = htevents

	def winner(self):
		if(self.atscore > self.htscore):
			return self.atname
		else:
			return self.htname

	def loser(self):
		if(self.atscore > self.htscore):
			return self.htname
		else:
			return self.atname

	def results(self):
		return ("{}: {} - {}: {}".format(self.atname,self.atscore,self.htname,self.htscore))

class Event(object):
	def __init__(self, point, playername):
		self.point = point
		self.playername = playername

