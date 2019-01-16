import datatool, game
from models import *

league = datatool.load_league("USFL")
league.draft_class = None
datatool.write_league(league)
