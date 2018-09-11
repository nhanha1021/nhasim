import json
from models import Player

FIRSTNAME_LABEL = "firstName"
LASTNAME_LABEL = "lastName"



def PlayerToJson(player):
	
	data = {
		FIRSTNAME_LABEL : player.firstName,
		LASTNAME_LABEL : player.lastName
	}
	return data

def JsonToPlayer(data):
	
	return Player(data[FIRSTNAME_LABEL], data[LASTNAME_LABEL])

def TeamToJson(team):

	pass

def JsonToTeam(data):

	pass

