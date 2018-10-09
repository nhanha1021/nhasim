import random

class Game(object):

	def __init__(self, awayTeam, homeTeam):
		self.awayTeam = awayTeam
		self.homeTeam = homeTeam
		self.awayScore = 0
		self.homeScore = 0


	def playGame(self):
		for player in self.awayTeam.allPlayers():
			poff = calcOff(player)
			pdef = calcDef(player)
			pts = poff-pdef
			if(pts >= 0):
				self.awayScore += pts
		for player in self.homeTeam.allPlayers():
			poff = calcOff(player)
			pdef = calcDef(player)
			pts = poff-pdef
			if(pts >= 0):
				self.homeScore += pts
		print("%s - %d\n%s - %d") % (self.awayTeam.teamName, self.awayScore, self.homeTeam.teamName, self.homeScore)
		if(self.awayScore > self.homeScore):
			return self.awayTeam
		else:
			return self.homeTeam

def calcOff(player):
	pts = 0
	off = player.offense
	for i in range(10):
		if(random.randint(0,300)<off):
			pts += 1
	return pts

def calcDef(player):
	pts = 0 
	dfn = player.defense
	for i in range(10):
		if(random.randint(0,300)<dfn):
			pts +=1
	return pts

