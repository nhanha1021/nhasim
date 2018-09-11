import json
from models import Player
from models import Team
from models import League

FIRSTNAME_LABEL = "firstName"
LASTNAME_LABEL = "lastName"
TEAMNAME_LABEL = "teamName"
ROSTER_LABEL = "roster"
LEAGUENAME_LABEL = "leagueName"
TEAMROSTER_LABEL = "teamRoster"

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

def LeagueToJson(league):
	data = {
		LEAGUENAME_LABEL : league.leagueName
	}
	teamRoster = []
	for team in league.teamRoster:
		teamRoster.append(TeamToJson(team))
	data[TEAMROSTER_LABEL] = teamRoster
	return data

def JsonToLeague(data):
	leagueName = data[LEAGUENAME_LABEL]
	jsonroster = data[TEAMROSTER_LABEL]
	teamRoster = []
	for jsonteam in jsonroster:
		teamRoster.append(JsonToTeam(jsonteam))
	return League(leagueName, teamRoster)


