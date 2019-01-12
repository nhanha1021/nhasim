import rostertool, game
from models import *
from seasonsim import PostseasonShell

league = rostertool.load_league("USFL")
teams = league.get_all_teams()[:8]
postseason = Postseason(teams)

shell = PostseasonShell(postseason)
shell.run()

