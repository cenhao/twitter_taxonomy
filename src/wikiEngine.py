from __future__ import print_function
import httplib, urllib
import json
import sys

class wikiEngine:
	def __init__(self):
		pass

	def _get_longest_phrase(self, *words):
		titles = ""
		cnt = 0
		phrases = list()

		for word in words:
			if cnt == 0:
				phrases.append(word)
			else:
				phrases.append(phrases[cnt-1] + ' ' + word)
			cnt = cnt + 1

		for i in range(0, len(phrases)):
			if i == 0:
				titles = phrases[i]
			else:
				titles += '|' + phrases[i]

		get_para = urllib.urlencode({
			'action' : 'query',
			'titles' : titles,
			'redirects' : '',
			'format' : 'json'
			})
		header = {'user_agent' : 'cenhao123 at gmail dot com'}

		try:
			conn = httplib.HTTPConnection('en.wikipedia.org', 80, timeout=3)
			conn.request('GET', '/w/api.php?' + get_para, headers = header)
		except httplib.HTTPException as e:
			print('HTTP connection failure: {:s}'.format(e), file = sys.stderr)
			return -1
		except:
			print('Unknow system failure', file = sys.stderr)
			return -2

		rsp = conn.getresponse()

		if rsp.status != 200:
			print('Requesting Wiki fails: {} {}'.format(rsp.status, rsp.reason), file = sys.stderr)
			return -3

		data = rsp.read()
		res = json.loads(data)

		normalized = dict()
		info = dict()
		redirects = dict()
		pages = res['query']['pages']

		for pageid in pages:
			if 'missing' not in pages[pageid]:
				info[pages[pageid]['title']] = pageid

		for pair in res['query']['redirects']:
			redirects[pair['from']] = pair['to']

		for pair in res['query']['normalized']:
			tmp = None
			if pair['to'] in redirects:
				tmp = redirects[pair['to']]
			else:
				tmp = pair['to']

			if tmp in info:
				normalized[pair['from']] = [tmp, info[tmp]]
		
		mx = -1
		for i in range(0, len(phrases)):
			if phrases[i] in normalized:
				mx = i

		return [phrases[i], normalized[phrases[mx]][0], normalized[phrases[mx]][1]]

	def getLinks(self, *phrases):
		pass
