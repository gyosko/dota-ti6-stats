# http://docs.python-guide.org/en/latest/scenarios/scrape/
import time as t
import requests as r
from lxml import html
from bs4 import BeautifulSoup as B

# Let the magic(finally!) begin?
base_url = 'http://www.dotabuff.com/esports'
pages = [
	'/events/121/series',
	'/leagues/4716/series',
	'/leagues/4716/series?page=2',
	'/events/112/series',
	'/leagues/4700/series'
]

all_match_ids = set()
for page in pages:
	t.sleep(1)
	p = r.get(base_url + page,headers = {'User-agent': 'Mozilla/5.0'})
	soup = B(p.content)
	for link in soup.find_all('a'):
		l = link.get('href').split('/')
		try:
			if(l[1]=='matches'):
				match_id = l[2]
				all_match_ids.add(match_id)
		except:
			pass

f = open('matchids.txt','w')
for match in all_match_ids:
	f.write(match + '\n')
f.close()