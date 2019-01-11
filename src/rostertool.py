from models import Player, Team, League, Season
import json, jsontool

LEAGUE_DATA_PATH = "/Users/johnshea/Repos/nhasim_python/data/"

def _to_file_name(name):
	return name.replace(" ","")+".json"

def write_league(league):
	data = jsontool.league_to_json(league)
	filename = _to_file_name(league.get_league_name())
	with open(LEAGUE_DATA_PATH+filename,'w') as datafile:
		json.dump(data, datafile)

def load_league(leagueName):
	filename = _to_file_name(leagueName)
	with open(LEAGUE_DATA_PATH+filename,'r') as datafile:
		data = json.load(datafile)
		return jsontool.json_to_league(data)

def write_season(season):
	data = jsontool.season_to_json(season)
	filename = _to_file_name(season.league.get_league_name()+"Season")
	with open(LEAGUE_DATA_PATH+filename,'w') as datafile:
		json.dump(data,datafile)

