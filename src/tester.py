import datatool, game, schedule
from models import *

teams = [team.get_team_name() for team in datatool.load_league("USFL").get_all_teams()]
schedule = schedule.make_schedule(teams)

for week in schedule:
	for game in week:
		print game

tdict = {}
for team in teams:
	tdict[team] = [0,0]


for team in teams:
	for week in schedule:
		for game in week:
			if(team == game[0]):
				tdict[team][0] += 1
			if(team == game[1]):
				tdict[team][1] += 1

for key, value in tdict.items():
	print key,value
