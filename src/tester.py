import rostertool, game
from models import *

league = rostertool.load_league("USFL")
game_results = rostertool.load_grs()
for game_result in game_results:
	print game_result.get_winner().get_team_name()

