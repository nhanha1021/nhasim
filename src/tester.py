import datatool, game, schedule
from models import *

league = datatool.load_league("USFL")
s = schedule.make_schedule(league.get_all_teams())
season = Season(league,s,0)
datatool.write_season(season)

season = datatool.load_season("USFL")
for week in season.schedule:
	for game in week:
		print game

