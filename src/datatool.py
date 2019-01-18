from models import Player,Team,League,DraftClass,Season,Postseason
from game import GameResult
import json

LEAGUE_DATA_PATH = "/Users/johnshea/Repos/nhasim_python/data/"

def _to_league_file_name(name):
	return name.replace(" ","")+"_league.json"

def _to_season_file_name(name):
	return name.replace(" ","")+"_season.json"

def write_league(league):
	data = _league_to_json(league)
	filename = _to_league_file_name(league.get_league_name())
	with open(LEAGUE_DATA_PATH+filename,'w') as datafile:
		json.dump(data, datafile)

def load_league(leagueName):
	filename = _to_league_file_name(leagueName)
	with open(LEAGUE_DATA_PATH+filename,'r') as datafile:
		data = json.load(datafile)
		return _json_to_league(data)

def write_season(season):
	data = _season_to_json(season)
	filename = _to_season_file_name(season.league.leagueName)
	with open(LEAGUE_DATA_PATH+filename,'w') as datafile:
		json.dump(data,datafile)

def load_season(season_name):
	filename = _to_season_file_name(season_name)
	with open(LEAGUE_DATA_PATH+filename,'r') as datafile:
		data = json.load(datafile)
		return _json_to_season(data) 

FIRSTNAME_LABEL = "firstName"
LASTNAME_LABEL = "lastName"
OFFENSE_LABEL = "offense"
DEFENSE_LABEL = "defense"
TEAMNAME_LABEL = "teamName"
ROSTER_LABEL = "roster"
LEAGUENAME_LABEL = "leagueName"
TEAMROSTER_LABEL = "teamRoster"
L_DRAFT_CLASS_LABEL = "draft_class"
L_PICKS_ADDED_LABEL = "picks_added"
SEASON_LEAGUENAME_LABEL = "leagueName"
SEASON_SCHEDULE_LABEL = "schedule"
SEASON_WEEK_LABEL = "week"
SEASON_STANDINGS_LABEL = "standings"
SEASON_RESULTS_LABEL = "results"
SEASON_POSTSEASON_LABEL = "postseason"
PS_TEAMS_LABEL = "teams"
PS_SEEDS_LABEL = "seeds"
PS_BRACKET_LABEL = "bracket"
PS_RESULTS_LABEL = "results"
PS_CUR_ROUND_LABEL = "cur_round"
PS_COMPLETE_LABEL = "complete"
GR_AWAY_TEAM = "away_team"
GR_HOME_TEAM = "home_team"
GR_AWAY_SCORE = "away_score"
GR_HOME_SCORE = "home_score"
GR_AWAY_EVENTS = "away_events"
GR_HOME_EVENTS = "home_events"
DC_NAME_LABEL = "class_name"
DC_RESULTS_LABEL = "results"
DC_CANDIDATES_LABEL = "candidates"
DC_FINISHED_LABEL = "finished"

def _to_tuple(s):
		s = s.replace("(","").replace(")","")
		l = s.split(",")
		return (int(l[0]),int(l[1]))

def _player_to_json(player):
	data = {
		FIRSTNAME_LABEL : player.firstName,
		LASTNAME_LABEL : player.lastName,
		OFFENSE_LABEL : player.offense,
		DEFENSE_LABEL : player.defense
	}
	return data

def _json_to_player(data):
	firstName = data[FIRSTNAME_LABEL]
	lastName = data[LASTNAME_LABEL]
	offense = data[OFFENSE_LABEL]
	defense = data[DEFENSE_LABEL]
	return Player(firstName,lastName, offense, defense)

def _team_to_json(team):
	data = {
		TEAMNAME_LABEL : team.teamName
	}
	roster = []
	for player in team.get_all_players():
		roster.append(_player_to_json(player))
	data[ROSTER_LABEL] = roster
	return data

def _json_to_team(data):
	team = Team(data[TEAMNAME_LABEL])
	jsonroster = data[ROSTER_LABEL]
	for jsonplayer in jsonroster:
		player = _json_to_player(jsonplayer)
		team.add_player(player)
	return team
	
def _league_to_json(league):
	data = {
		LEAGUENAME_LABEL : league.leagueName,
		L_DRAFT_CLASS_LABEL : None,
		L_PICKS_ADDED_LABEL : league.picks_added
	}
	teamRoster = []
	for team in league.get_all_teams():
		teamRoster.append(_team_to_json(team))
	data[TEAMROSTER_LABEL] = teamRoster
	if(league.draft_class != None):
		data[L_DRAFT_CLASS_LABEL] = _draft_class_to_json(league.draft_class)
	return data

def _json_to_league(data):
	league = League(data[LEAGUENAME_LABEL])
	jsonroster = data[TEAMROSTER_LABEL]
	for jsonteam in jsonroster:
		team = _json_to_team(jsonteam)
		league.add_team(team)
	draft_class = None
	if(data[L_DRAFT_CLASS_LABEL]!= None):
		draft_class = _json_to_draft_class(data[L_DRAFT_CLASS_LABEL])
	league.draft_class = draft_class
	league.picks_added = data[L_PICKS_ADDED_LABEL]
	return league

def _season_to_json(season):
	data = {
		SEASON_LEAGUENAME_LABEL : season.league.leagueName,
		SEASON_WEEK_LABEL : season.week,
		SEASON_SCHEDULE_LABEL : season.schedule,
		SEASON_STANDINGS_LABEL : season.standings,
		SEASON_POSTSEASON_LABEL : None
	}

	jsonresults = {}
	for key,result in season.results.items():
		jsonresults[str(key)] = _game_result_to_json(result)
	data[SEASON_RESULTS_LABEL] = jsonresults

	if(season.postseason != None):
		data[SEASON_POSTSEASON_LABEL] = _postseason_to_json(season.postseason)
	
	return data

def _json_to_season(data):

	league = load_league(data[SEASON_LEAGUENAME_LABEL])

	schedule = data[SEASON_SCHEDULE_LABEL]
	for week in range(len(schedule)):
		for game in range(len(schedule[week])):
			schedule[week][game][2] = tuple(schedule[week][game][2])
			schedule[week][game] = tuple(schedule[week][game])

	week = data[SEASON_WEEK_LABEL]
	season = Season(league, schedule, week)

	season.standings = data[SEASON_STANDINGS_LABEL]

	results = {}
	for key,jsonresult in data[SEASON_RESULTS_LABEL].items():
		results[_to_tuple(key)] = _json_to_game_result(jsonresult)
	season.results = results

	postseason = None
	if(data[SEASON_POSTSEASON_LABEL] != None):
		postseason = _json_to_postseason(data[SEASON_POSTSEASON_LABEL])
	season.postseason = postseason

	return season

def _postseason_to_json(postseason):
	data = {
		PS_SEEDS_LABEL : postseason.seeds,
		PS_BRACKET_LABEL : postseason.bracket,
		PS_CUR_ROUND_LABEL : postseason.cur_round,
		PS_COMPLETE_LABEL : postseason.complete
	}

	jsonteams = {}
	for team_name,team in postseason.teams.items():
		jsonteams[team_name] = _team_to_json(team)
	data[PS_TEAMS_LABEL] = jsonteams

	jsonresults = {}
	for key,result in postseason.results.items():
		jsonresults[str(key)] = _game_result_to_json(result)
	data[PS_RESULTS_LABEL] = jsonresults

	return data

def _json_to_postseason(data):

	seeds = data[PS_SEEDS_LABEL]
	cur_round = data[PS_CUR_ROUND_LABEL]
	complete = data[PS_COMPLETE_LABEL]

	bracket = data[PS_BRACKET_LABEL]
	for rnd in range(len(bracket)):
		for game in range(len(bracket[rnd])):
			bracket[rnd][game][2] = tuple(bracket[rnd][game][2])
			bracket[rnd][game] = tuple(bracket[rnd][game])

	results = {}
	for key, jsonresult in data[PS_RESULTS_LABEL].items():
		results[_to_tuple(key)] = _json_to_game_result(jsonresult)

	teams = {}
	for team_name,jsonteam in data[PS_TEAMS_LABEL].items():
		teams[team_name] = _json_to_team(jsonteam)

	postseason = Postseason([])
	postseason.seeds = seeds
	postseason.bracket = bracket
	postseason.results = results
	postseason.cur_round = cur_round
	postseason.complete = complete
	postseason.teams = teams
	postseason.results = results

	return postseason

def _game_result_to_json(game_result):
	data = {
		GR_AWAY_TEAM : game_result.away_team_name,
		GR_AWAY_SCORE : game_result.away_score,
		GR_AWAY_EVENTS : game_result.away_events,
		GR_HOME_TEAM : game_result.home_team_name,
		GR_HOME_SCORE : game_result.home_score,
		GR_HOME_EVENTS : game_result.home_events
	}
	return data

def _json_to_game_result(data):
	away_team_name = data[GR_AWAY_TEAM]
	away_score = data[GR_AWAY_SCORE]
	away_events = data[GR_AWAY_EVENTS]
	home_team_name = data[GR_HOME_TEAM]
	home_score = data[GR_HOME_SCORE]
	home_events = data[GR_HOME_EVENTS]
	return GameResult(away_team_name, away_score, away_events, home_team_name, home_score, home_events)

def _draft_class_to_json(draft_class):
	data = {
		DC_NAME_LABEL : draft_class.class_name,
		DC_FINISHED_LABEL : draft_class.finished
	}
	jsonresults = []
	for member,team_name in draft_class.results:
		jsonresults.append((_player_to_json(member),team_name))
	data[DC_RESULTS_LABEL] = jsonresults
	jsoncandidates = {}
	for count,candidate in draft_class.candidates.items():
		jsoncandidates[count] = _player_to_json(candidate)
	data[DC_CANDIDATES_LABEL] = jsoncandidates
	return data
		
def _json_to_draft_class(data):
	class_name = data[DC_NAME_LABEL]
	draft_class = DraftClass(class_name)
	finished = data[DC_FINISHED_LABEL]
	draft_class.finished = finished
	results = []
	for jsonmember,team_name in data[DC_RESULTS_LABEL]:
		results.append((_json_to_player(jsonmember),team_name))
	draft_class.results = results
	candidates = {}
	for count,jsoncandidate in data[DC_CANDIDATES_LABEL].items():
		candidates[int(count)] = _json_to_player(jsoncandidate)
	draft_class.candidates = candidates
	return draft_class



