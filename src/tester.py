from models import League
import schedule, rostertool

league = rostertool.loadLeague("USFL")
s = schedule.make_schedule([i for i in range(1,17)])

i = 0
for w in s:
	print w




