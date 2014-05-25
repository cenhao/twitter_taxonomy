from __future__ import print_function
import httplib, urllib
import json
import sys
import lru

class wikiEngine:
	def __init__(self):
		pass

	@lru.lru_cache(maxsize = 10000000)#10,000,000 * 25 = 250 mb
	def _check_phrase(self, phrase):
		'''@retval: [pageid, normalized_name, redirect_name]'''
		get_para = urllib.urlencode({
			'action' : 'query',
			'titles' : phrase,
			'redirects' : '',
			'format' : 'json'
			})
		header = {'user_agent' : 'cenhao123 at gmail dot com'}

		try:
			conn = httplib.HTTPConnection('en.wikipedia.org', 80, timeout=3)
			conn.request('GET', '/w/api.php?' + get_para, headers = header)
			rsp = conn.getresponse()

			if rsp.status != 200:
				print('Requesting Wiki fails: {} {}'.format(rsp.status, rsp.reason), file = sys.stderr)
				failcnt = failcnt + 1

			data = rsp.read()
		except httplib.HTTPException as e:
			print('HTTP connection failure: {:s}'.format(e), file = sys.stderr)
			return -1
		except:
			print('Unknow system failure', file = sys.stderr)
			return -1

		rsp = conn.getresponse()

		if rsp.status != 200:
			print('Requesting Wiki fails: {} {}'.format(rsp.status, rsp.reason), file = sys.stderr)
			return -1

		data = rsp.read()
		res = json.loads(data)
		res = res['query']
		ret = []

		ret.append(0)
		for pageid in res['pages']:
			ret[0] = pageid

		if ret[0] < 0:#no such entry
			return -2

		if 'normalized' in res:
			ret.append(res['normalized'][0]['to'])
		else:
			ret.append(phrase)

		if 'redirects' in res:
			ret.append(res['redirects'][0]['to'])
		else:
			ret.append(ret[1])

	return ret

	def get_longest_phrase(self, *words):
		'''Use the words to generate phrases and query wiki
		to see if any of those phrases make sense. If yes
		return the longest one as a list:
		[length_of_phrase, phrase, [pageid, normalized_name, redirect_name]]'''
		cnt = 0
		phrases = list()

		for word in words:
			if cnt == 0:
				phrases.append(word)
			else:
				phrases.append(phrases[cnt-1] + ' ' + word)
			cnt = cnt + 1

		lengthOfPhrase = 0

		for i in range(len(phrases)-1, -1, -1):
			ret = _check_phrase(phrases[i])

			if isinstance(ret, int):#failure or item not exists
				if ret == -1:#failure
					failcnt = 0

					while failure < 3:
						ret = _check_phrase.__wrapped__(phrases[i])

						if isinstance(ret, int) and ret == -1:
							failcnt = failure + 1
						else:
							break

			if isinstance(ret, list):
				lengthOfPhrase = i + 1
				break

		return [lengthOfPhrase, phrases[i], ret]

	@lru.lru_cache(maxsize = 15000)
	def get_links(self, pageid):
		get_para = urllib.urlencode({
			'action' : 'query',
			'list' : 'backlinks',
			'bllimit' : 'max',
			'blpageid' : ret[2],
			'blfilterredir' : 'nonredirects',
			'bldir' : 'ascending',
			'format' : 'json'
			})
		header = {'user_agent' : 'cenhao123 at gmail dot com'}
		failcnt = 0
		data = 0
		backlinks = []

		while True:
			if failcnt > 3: return -1
			try:
				conn = httplib.HTTPConnection('en.wikipedia.org', 80, timeout=3)
				conn.request('GET', '/w/api.php?' + get_para, headers = header)
				rsp = conn.getresponse()

				if rsp.status != 200:
					print('Requesting Wiki fails: {} {}'.format(rsp.status, rsp.reason), file = sys.stderr)
					failcnt = failcnt + 1
					continue

				data = rsp.read()
			except httplib.HTTPException as e:
				print('HTTP connection failure: {:s}'.format(e), file = sys.stderr)
				failcnt = failcnt + 1
				continue
			except:
				print('Unknow system failure', file = sys.stderr)
				failcnt = failcnt + 1
				continue

			failcnt = 0 #reset fail counter
			res = json.loads(data)

			for blk in res['query']['backlinks']:
				print('pageid: {:d}'.format(blk['pageid']))#for debuging
				backlinks.append(blk['pageid'])

			if 'query-continue' in res:
				get_para = urllib.urlencode({
					'action' : 'query',
					'list' : 'backlinks',
					'bllimit' : 'max',
					'blpageid' : ret[2],
					'blfilterredir' : 'nonredirects',
					'format' : 'json',
					'bldir' : 'ascending',
					'blcontinue' : res['query-continue']['backlinks']['blcontinue'],
					})
			else:
				break

		return [backlinks]

	def test_phrase_and_get_link(self, *words):
		ret = self.get_longest_phrase(*words)

		if ret[0] <= 0:#can't find any phrase
			retrun -1

		lnks = self.get_links(ret[0])
		return [ret[0], 
