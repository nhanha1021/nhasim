from models import League
from tabulate import tabulate
import rostertool, schedule, sys

league_name = sys.argv[1]
#Load league
league = rostertool.loadLeague(league_name)

#TODO: Fix schedule 
season_schedule = schedule.make_schedule(league.allTeams())
new_schedule = []
for week in season_schedule:
	for game in week:
		new_schedule.append(game)

#Define the standings
standings = {}
for team in league.allTeams():
	standings[team.teamName] = [0,0]

#Play each game
for game in new_schedule:
	game_result = game.play_game()
	standings[game_result.winner()][0] += 1
	standings[game_result.loser()][1] += 1

#Sort and print standings
sorted_standings = []
for team, record in standings.items():
	sorted_standings.append([team, record[0], record[1]])
sorted_standings.sort(key=lambda x:int(x[1]), reverse=True)
for row in sorted_standings:
	print("{}: {}-{}".format(row[0],row[1],row[2]))

