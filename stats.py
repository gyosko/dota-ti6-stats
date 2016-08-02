import csv,ast,json

data = csv.reader(open("output.csv","r"))
dictionary = {}
for row in data:
	try:
		d = ast.literal_eval(row[1])
		dictionary[row[0]] = d
	except:
		continue
heroes = [h for h in dictionary['played_hero'].keys()]
players = [p for p in dictionary['dif_heroes_player'].keys()]
teams = [t for t in dictionary['assists_team'].keys()]

eroi = json.load(open('heroes.json','r'))
def get_hero_name(id):
	for e in eroi:
		if(e['id']==id):
			return e['localized_name']
heroes_stats = {}
for hero_id in heroes:
	hero_name = get_hero_name(hero_id)
	kills = dictionary['kill_hero'][hero_id]
	assists = dictionary['assists_hero'][hero_id]
	deaths = dictionary['deaths_hero'][hero_id]
	gpm = dictionary['gpm_hero'][hero_id]
	played_games = len(kills)
	try:
		picked = dictionary['picked'][hero_id]
	except:
		picked = 0
	try:
		banned = dictionary['banned'][hero_id]
	except:
		banned = 0
	try:
		won = dictionary['win_hero'][hero_id]
	except:
		won = 0
	heroes_stats[hero_name] = {
		'gpm_avg' : round(sum(gpm) / played_games,2),
		'max_gpm' : max(gpm),
		'kills_avg' : round(sum(kills) / played_games,2),
		'max_kills' : max(kills),
		'assists_avg' : round(sum(assists) / played_games,2),
		'max_assists' : max(assists),
		'deaths_avg' : round(sum(deaths) / played_games,2),
		'max_deaths' : max(deaths),
		'min_deaths' : min(deaths),
		'picked' : picked,
		'banned' : banned,
		'win_pct' : round(won/played_games,2)
	}
players_stats = {}
for player_id in players:
	player_name = player_id + 76561197960265728 
	kills = dictionary['kill_player'][player_id]
	assists = dictionary['assists_player'][player_id]
	deaths = dictionary['death_player'][player_id]
	gpm = dictionary['gpm_player'][player_id]
	played_games = len(kills)
	players_stats[player_name] = {
		'gpm_avg' : round(sum(gpm) / played_games,2),
		'max_gpm' : max(gpm),
		'kills_avg' : round(sum(kills) / played_games,2),
		'max_kills' : max(kills),
		'assists_avg' : round(sum(assists) / played_games,2),
		'max_assists' : max(assists),
		'deaths_avg' : round(sum(deaths) / played_games,2),
		'max_deaths' : max(deaths)
	}
def retrieve(dizio,chiave,valore,doppi):
	for k in dizio.keys():
		check = dizio[k][chiave]
		if(check==valore and k not in doppi):
			return k
file_finale = open('finals.txt','w')
# Heroes
stuffs = ['gpm_avg','max_gpm','kills_avg','max_kills','assists_avg','max_assists','deaths_avg','max_deaths','min_deaths','picked','banned','win_pct']
values = {s:[] for s in stuffs}
for hero in heroes_stats.keys():
	for s in stuffs:
		values[s].append(heroes_stats[hero][s])
for v in values.keys():
	values[v] = sorted(values[v])[::-1]
	if(v=='min_deaths' or v=='deaths_avg'):
		values[v] = sorted(values[v])
for v in values.keys():
	file_finale.write(str(v) + '\n')
	lista = values[v][:5] # Top 5 ans
	eroi = []
	for l in lista:
		eroe = retrieve(heroes_stats,v,l,eroi)
		eroi.append(eroe)
		file_finale.write(str(eroe) + ' ' + str(l) + ' - ')
	file_finale.write('\n')

# Players
stuffs = ['gpm_avg','max_gpm','kills_avg','max_kills','assists_avg','max_assists','deaths_avg','max_deaths']
values = {s:[] for s in stuffs}
for player in players_stats.keys():
	for s in stuffs:
		values[s].append(players_stats[player][s])
for v in values.keys():
	values[v] = sorted(values[v])[::-1]
	if(v=='min_deaths' or v=='deaths_avg'):
		values[v] = sorted(values[v])
for v in values.keys():
	file_finale.write(str(v) + '\n')
	lista = values[v][:5] # Top 5 ans
	eroi = []
	for l in lista:
		eroe = retrieve(players_stats,v,l,eroi)
		eroi.append(eroe)
		file_finale.write(str(eroe) + ' ' + str(l) + ' - ')
	file_finale.write('\n')
