import game, rostertool, newschedule

league = rostertool.load_league("USFL")
schedule = newschedule.make_schedule(league.get_all_teams())

count = 0
for week in schedule:
	for game in week:
		print(game)
		count+=1

print count

