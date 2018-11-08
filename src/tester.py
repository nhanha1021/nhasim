from models import League
import schedule, rostertool

league = rostertool.loadLeague("USFL")
s = schedule.make_schedule(league.allTeams())

i = 0
for w in s:
	i += 1
	print("\nWeek {}".format(i))
	for g in w:
		print("{} @ {}".format(g[0].teamName,g[1].teamName))




