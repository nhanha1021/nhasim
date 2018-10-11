import random

class Game(object):

	def __init__(self, awayTeam, homeTeam):
		self.awayTeam = awayTeam
		self.homeTeam = homeTeam
		self.awayScore = 0
		self.homeScore = 0

	def playGame(self):
		self.play(3)
		while(self.awayScore == self.homeScore):
			self.play(1)
		return self.getResult()

	def play(self, n):
		for i in range(n):
			for player in self.awayTeam.allPlayers():
				self.awayScore += calcScore(player, self.homeTeam.allPlayers())
			for player in self.homeTeam.allPlayers():
				self.homeScore += calcScore(player, self.awayTeam.allPlayers())


	def getResult(self):
		if(self.awayScore > self.homeScore):
			return GameResult(self.awayTeam.teamName, self.awayScore, self.homeTeam.teamName, self.homeScore)
		else:
			return GameResult(self.homeTeam.teamName, self.homeScore, self.awayTeam.teamName, self.awayScore)

class GameResult(object):
	def __init__(self, winner, wscore, loser, lscore):
		self.winner = winner
		self.loser = loser
		self.wscore = wscore
		self.lscore = lscore

	def finalScore(self):
		return ("%s %d \n%s %d") % (self.winner, self.wscore, self.loser, self.lscore)

def calcScore(player, defense):
	d = random.sample(defense, 3)
	dsum = sum(p.defense for p in d)
	i = random.randint(0, dsum)
	if(i<player.offense):
		return 1
	return 0
