from seasonsim import SeasonShell
import rostertool,schedule
from models import Season

season = rostertool.load_season("USFL")
shell = SeasonShell(season)
shell.run()
rostertool.write_season(season)
print("Wrote season!")


