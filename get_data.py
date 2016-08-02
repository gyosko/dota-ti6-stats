import requests as r
import time as t
import json
import csv
api_key = 'steam-api-key'
base_url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1/'

f = open('matchids.txt','r')
output = {
	'picked' : {},
	'banned' : {},
	'win_hero' : {},
	'lost_hero' : {},
	'played_hero' : {},
	'kill_hero': {},
	'assists_hero' : {},
	'deaths_hero' : {},
	'last_hits_hero' : {},
	'gpm_hero' : {},
	'team_win' : {},
	'team_lost' : {},
	'team_played' : {},
	'kills_team' : {},
	'deaths_team' : {},
	'assists_team' : {},
	'longest_win_team' : 0,
	'shortest_win_team' : float('inf'),
	'dif_heroes_team' : {},
	'kill_player' : {},
	'death_player' : {},
	'assists_player' : {},
	'last_hits_player' : {},
	'gpm_player' : {},
	'dif_heroes_player' : {}
}
def add_one(lista,oggetto):
	try:
		lista[oggetto] += 1
	except:
		lista[oggetto] = 1
	return lista
def add_hero(tipo,team,hero):
	try:
		output[tipo][team].add(hero)
	except:
		output[tipo][team] = set([hero])
def add_value(tipo,who,kills):
	try:
		output[tipo][who].append(kills)
	except:
		output[tipo][who] = [kills]
def add_duration(time):
	longest = output['longest_win_team']
	shortest = output['shortest_win_team']
	if(time>longest):
		output['longest_win_team'] = time
	if(time<shortest):
		output['shortest_win_team'] = time
errori = open('errori.txt','w')
for match_id in f.readlines():
	print('Starting...')
	t.sleep(2)
	m = str(int(match_id))
	p = r.get(base_url + '?match_id=' + m + '&key=' + api_key)
	status_code = p.status_code
	while status_code!=200:
		t.sleep(5)
		p = r.get(base_url + '?match_id=' + m + '&key=' + api_key)
		status_code = p.status_code
	data = p.json()['result']
	try:
		dire = data['dire_name']
		radiant = data['radiant_name']
		tmp = data['picks_bans']
		tmp = data['players']
		tmp = data['radiant_win']
	except:
		errori.write(match_id)
		continue
	dire_heroes = []
	radiant_heroes = []
	dire_totals = {}
	radiant_totals = {}
	for hero in data['picks_bans']:
		if(hero['is_pick']):
			output['picked'] = add_one(output['picked'],hero['hero_id'])
			if(hero['team']==0): # Radiant picked
				add_hero('dif_heroes_team',radiant,hero['hero_id'])
				radiant_heroes.append(hero['hero_id'])
			else:
				add_hero('dif_heroes_team',dire,hero['hero_id'])
				dire_heroes.append(hero['hero_id'])
		else:
			output['banned'] = add_one(output['banned'],hero['hero_id'])
	for player in data['players']:
		hero_played = player['hero_id']
		player_id = player['account_id']
		kills = player['kills']
		deaths = player['deaths']
		assists = player['assists']
		gpm = player['gold_per_min']
		last_hits = player['last_hits']

		add_hero('dif_heroes_player',player_id,hero_played)

		add_value('kill_hero',hero_played,kills)
		add_value('kill_player',player_id,kills)
		add_value('last_hits_hero',hero_played,last_hits)
		add_value('last_hits_player',player_id,last_hits)
		add_value('gpm_hero',hero_played,gpm)
		add_value('gpm_player',player_id,gpm)
		add_value('assists_hero',hero_played,assists)
		add_value('assists_player',player_id,assists)
		add_value('death_player',player_id,deaths)
		add_value('deaths_hero',hero_played,deaths)

		if(hero_played in radiant_heroes):
			try:
				radiant_totals['assists'] += assists
				radiant_totals['kills'] += kills
				radiant_totals['deaths'] += deaths
			except:
				radiant_totals['assists'] = assists
				radiant_totals['kills'] = kills
				radiant_totals['deaths'] = deaths
		else:
			try:
				dire_totals['assists'] += assists
				dire_totals['kills'] += kills
				dire_totals['deaths'] += deaths
			except:
				dire_totals['assists'] = assists
				dire_totals['kills'] = kills
				dire_totals['deaths'] = deaths
	add_value('assists_team',radiant,radiant_totals['assists'])
	add_value('kills_team',radiant,radiant_totals['kills'])
	add_value('deaths_team',radiant,radiant_totals['deaths'])

	add_value('assists_team',dire,dire_totals['assists'])
	add_value('kills_team',dire,dire_totals['kills'])
	add_value('deaths_team',dire,dire_totals['deaths'])

	try:
		output['team_played'][dire] += 1
	except:
		output['team_played'][dire] = 1
	try:
		output['team_played'][radiant] += 1
	except:
		output['team_played'][radiant] = 1
	add_duration(data['duration'])
	if(data['radiant_win']):
		try:
			output['team_win'][radiant] += 1
		except:
			output['team_win'][radiant] = 1
		try:
			output['team_lost'][dire] += 1
		except:
			output['team_lost'][dire] = 1
		for eroe in radiant_heroes:
			output['win_hero'] = add_one(output['win_hero'],eroe)
			output['played_hero'] = add_one(output['played_hero'],eroe)
		for eroe in dire_heroes:
			output['lost_hero'] = add_one(output['lost_hero'],eroe)
			output['played_hero'] = add_one(output['played_hero'],eroe)
	else:
		try:
			output['team_win'][dire] += 1
		except:
			output['team_win'][dire] = 1
		try:
			output['team_lost'][radiant] += 1
		except:
			output['team_lost'][radiant] = 1
		for eroe in radiant_heroes:
			output['lost_hero'] = add_one(output['lost_hero'],eroe)
			output['played_hero'] = add_one(output['played_hero'],eroe)
		for eroe in dire_heroes:
			output['win_hero'] = add_one(output['win_hero'],eroe)
			output['played_hero'] = add_one(output['played_hero'],eroe)
	print('Done...')
w = csv.writer(open("output.csv", "w"))
for key, val in output.items():
    w.writerow([key, val])