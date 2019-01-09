from models import Player
from models import Team
from models import League
import json, jsontool, randomname, random

LEAGUE_DATA_PATH = "/Users/johnshea/Repos/nhasim_python/data/"

def writeLeague(league):
	data = jsontool.league_to_json(league)
	filename = _to_file_name(league.get_league_name())
	with open(LEAGUE_DATA_PATH+filename,'w') as datafile:
		json.dump(data, datafile)

def loadLeague(leagueName):
	filename = _to_file_name(leagueName)
	with open(LEAGUE_DATA_PATH+filename,'r') as datafile:
		data = json.load(datafile)
		return jsontool.json_to_league(data)

def _to_file_name(name):
	return name.replace(" ","")+".json"