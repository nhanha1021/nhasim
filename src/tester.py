from seasonsim import Season, SeasonShell
import rostertool,schedule

league = rostertool.load_league("USFL")
schedule = schedule.make_schedule(league.get_all_teams())
season = Season(league, schedule, 0)
shell = SeasonShell(season)
shell.run()


