import datatool, game
from models import *

league = datatool.load_league("USFL")
game_results = datatool.load_grs()
for game_result in game_results:
	print game_result.get_winner().get_team_name()

