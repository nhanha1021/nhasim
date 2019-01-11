from seasonsim import SeasonShell
import rostertool,schedule
from models import Season

league = rostertool.load_league("USFL")
schedule = schedule.make_schedule(league.get_all_teams())
season = Season(league, schedule, 0)
shell = SeasonShell(season)
shell.run()
rostertool.write_season(season)
print("Wrote season!")


