from models import Player
from models import Team
from models import League
import json
import jsontool

PLAYER_DATA_PATH = "/Users/johnshea/Repos/nhasim_python/player_data/"
TEAM_DATA_PATH = "/Users/johnshea/Repos/nhasim_python/team_data/"
LEAGUE_DATA_PATH = "/Users/johnshea/Repos/nhasim_python/league_data/"

def writePlayer(player):

	data = jsontool.PlayerToJson(player)
	filename = formatName(player.fullName())
	with open(PLAYER_DATA_PATH+filename,'w') as datafile:
		json.dump(data, datafile)

def loadPlayer(playerName):

	filename = formatName(playerName)
	with open(PLAYER_DATA_PATH+filename,'r') as datafile:
		data = json.load(datafile)
		return jsontool.JsonToPlayer(data)

def writeTeam(team):

	data = jsontool.TeamToJson(team)
	filename = formatName(team.teamName)
	with open(TEAM_DATA_PATH+filename,'w') as datafile:
		json.dump(data, datafile)

def loadTeam(teamName):

	filename = formatName(teamName)
	with open(TEAM_DATA_PATH+filename,'r') as datafile:
		data = json.load(datafile)
		return jsontool.JsonToTeam(data)

def writeLeague(league):

	data = jsontool.LeagueToJson(league)
	filename = formatName(league.leagueName)
	with open(TEAM_DATA_PATH+filename,'r') as datafile:
		json.dump(data, datafile)

def loadLeague(leagueName):
	filename = formatName(leagueName)
	with open(LEAGUE_DATA_PATH+filename,'r') as datafile:
		data = json.load(datafile)
		return jsontool.JsonToLeague(data)

def formatName(name):

	return name.replace(" ","")+".json"