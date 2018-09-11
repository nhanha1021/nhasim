import json
from models import Player
from models import Team

FIRSTNAME_LABEL = "firstName"
LASTNAME_LABEL = "lastName"
TEAMNAME_LABEL = "teamName"
ROSTER_LABEL = "roster"

def PlayerToJson(player):
	
	data = {
		FIRSTNAME_LABEL : player.firstName,
		LASTNAME_LABEL : player.lastName
	}
	return data

def JsonToPlayer(data):

	firstName = data[FIRSTNAME_LABEL]
	lastName = data[LASTNAME_LABEL]
	return Player(firstName,lastName)

def TeamToJson(team):

	data = {
		TEAMNAME_LABEL : team.teamName
	}
	roster = []
	for player in team.roster:
		roster.append(PlayerToJson(player))
	data[ROSTER_LABEL] = roster
	return data

def JsonToTeam(data):

	teamName = data[TEAMNAME_LABEL]
	jsonroster = data[ROSTER_LABEL]
	roster = []
	for jsonplayer in jsonroster:
		roster.append(JsonToPlayer(jsonplayer))
	return Team(teamName, roster)




