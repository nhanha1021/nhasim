import random

def play_game(away_team, home_team):

	def play(away_team, home_team):

		def calc_event(player, team_defense):
			d_sample = random.sample(team_defense, 3)
			d_sum = sum(player.get_defense() for player in d_sample)
			i = random.randint(0,d_sum)
			if(i < player.get_offense()):
				return (1, player.get_full_name())
			return (0, player.get_full_name())

		away_events = []
		home_events = []

		for player in away_team.get_all_players():
			event = calc_event(player, home_team.get_all_players())
			away_events.append(event)
		for player in home_team.get_all_players():
			event = calc_event(player, away_team.get_all_players())
			home_events.append(event)

		return (away_events, home_events)

	def calc_points(events):
		points = 0
		for event in events:
			points += event[0]
		return points

	away_score = 0
	home_score = 0
	away_events = []
	home_events = []

	for i in range(3):
		outcome = play(away_team, home_team)
		away_events += outcome[0]
		home_events += outcome[1]
		away_score += calc_points(away_events)
		home_score += calc_points(home_events)
	while(away_score == home_score):
		outcome = play(away_team, home_team)
		away_events += outcome[0]
		home_events += outcome[1]
		away_score += calc_points(away_events)
		home_score += calc_points(home_events)		

	return GameResult(away_team, away_score, away_events, home_team, home_score, home_events)

class GameResult(object):

	def __init__(self, away_team, away_score, away_events, home_team, home_score, home_events):
		self.away_team = away_team
		self.away_score = away_score
		self.away_events = away_events
		self.home_team = home_team
		self.home_score = home_score
		self.home_events = home_events

	def get_winner(self):
		if(self.away_score > self.home_score):
			return self.away_team
		else:
			return self.home_team

	def get_loser(self):
		if(self.away_score < self.home_score):
			return self.away_team
		else:
			return self.home_team

	def get_away_team(self):
		return self.away_team

	def get_home_team(self):
		return self.home_team

	def get_away_score(self):
		return self.away_score

	def get_home_score(self):
		return self.home_score

	def get_results(self):
		return ("{}: {} - {}: {}".format(self.away_team.get_team_name(), self.away_score, self.home_team.get_team_name(), self.home_score))






