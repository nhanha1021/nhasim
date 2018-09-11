from models import Player
import json
import jsontool

PLAYER_DATA_PATH = "/Users/johnshea/Repos/nhasim_python/player_data/"
TEAM_DATA_PATH = "/Users/johnshea/Repos/nhasim_python/team_data/"

def writePlayer(player):

	data = jsontool.PlayerToJson(player)
	filename = formatName(player.getFullName())
	with open(PLAYER_DATA_PATH+filename,'w') as datafile:
		json.dump(data, datafile)

def loadPlayer(playerName):

	filename = formatName(playerName)
	with open(PLAYER_DATA_PATH+filename,'r') as datafile:
		data = json.load(datafile)
		return jsontool.JsonToPlayer(data)

def formatName(name):

	return name.replace(" ","")+".json"