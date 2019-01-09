import random

def play_game(away_team, home_team):

	def play(away_team, home_team):

		away_events = []
		home_events = []

		def calc_event(player, team_defense):
			d_sample = random.sample(team_defense, 3)
			d_sum = sum(player.get_defense() for player in d_sample)
			i = random.randint(0,d_sum)
			if(i < player.get_offense()):
				return (1, player.get_full_name())
			return (0, player.get_full_name())

		for player in away_team.get_all_players():
			point, name = calc_event(player, home_team.get_all_players())
			away_events.append([point, name])
		for player in home_team.get_all_players():
			point, name = calc_event(player, away_team.get_all_players())
			home_events.append([point, name])

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
		play(away_team, home_team)
		away_events += outcome[0]
		home_events += outcome[1]
		away_score += calc_points(away_events)
		home_score += calc_points(home_events)		

	print("{}:{} {}:{}".format(away_team.get_team_name(), away_score, home_team.get_team_name(), home_score))


