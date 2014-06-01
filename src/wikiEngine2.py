from __future__ import print_function
import httplib, urllib, urllib2
import threading
import json
import sys
import lru
import random

class wikiEngine2:
	def __init__(self):
		self._proxy_list = {}
		self.engine_lock = threading.Lock();
		pass

	def set_proxy(self, proxy_url, port):
		self.engine_lock.acquire()
		self._proxy_list[threading.current_thread().ident] = [proxy_url, port]
		self.engine_lock.release()

	def del_proxy(self):
		del self._proxy_list[threading.current_thread().ident]

	@lru.lru_cache(maxsize = 10000000)#10,000,000 * 25 = 250 mb
	def _check_phrase(self, phrase):
		'''
		@retval: [pageid, normalized_name, redirect_name]
		'''
		get_para = urllib.urlencode({
			'action' : 'query',
			'titles' : phrase,
			'redirects' : '',
			'format' : 'json'
			})
		header = {'user_agent' : random.random()}

		try:
			opener = 0;

			if threading.current_thread().ident in self._proxy_list:
				proxy_handler = urllib2.ProxyHandler({'http' : "{0:s}:{1:d}".format(self._proxy_list[threading.current_thread().ident][0],
					self._proxy_list[threading.current_thread().ident][1])})
				opener = urllib2.build_opener(proxy_handler)
			else:
				opener = urllib2.build_opener()

			req = urllib2.Request('http://en.wikipedia.org/w/api.php?' + get_para, headers=header);
			rsp = opener.open(req, timeout=5)

			if rsp.getcode() != 200:
				print('Requesting Wiki fails: {0}'.format(rsp.getcode()), file = sys.stderr)
				failcnt = failcnt + 1

			data = rsp.read()
			res = json.loads(data)
		except urllib2.HTTPError as e:
			print('HTTP Error: {0:d} {1:s}'.format(e.code, e.reason), file=sys.stderr)
			return -1
		except urllib2.URLError as e:
			print('URL Error: {0:s}'.format(e.reason), file = sys.stderr)
			return -1
		except:
			print('Unknow system failure', file = sys.stderr)
			return -1

		res = res['query']
		ret = []

		ret.append(0)
		for pageid in res['pages']:
			ret[0] = int(pageid)

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
			ret = self._check_phrase(phrases[i])

			if isinstance(ret, int):#failure or item not exists
				if ret == -1:#failure
					failcnt = 0

					while failcnt < 3:
						ret = self._check_phrase.__wrapped__(self, phrases[i])

						if isinstance(ret, int) and ret == -1:
							failcnt = failcnt + 1
						else:
							break

					if failcnt >= 3:
						print("get_longest_phrase encounter an error", file=sys.stderr)
						return -1

			if isinstance(ret, list):
				lengthOfPhrase = i + 1
				break
			else:
				lengthOfPhrase = -2

		return [lengthOfPhrase, phrases[i], ret]

	@lru.lru_cache(maxsize = 15000)
	def get_links(self, pageid):
		get_para = urllib.urlencode({
			'action' : 'query',
			'list' : 'backlinks',
			'bllimit' : 'max',
			'blpageid' : pageid,
			'blfilterredir' : 'nonredirects',
			'bldir' : 'ascending',
			'format' : 'json'
			})
		header = {'user_agent' : random.random()}
		failcnt = 0
		data = 0
		backlinks = []

		opener = 0

		try:
			if threading.current_thread().ident in self._proxy_list:
				proxy_handler = urllib2.ProxyHandler({'http' : '{0:s}:{1:d}'.format(self._proxy_list[threading.current_thread().ident][0],
					self._proxy_list[threading.current_thread().ident][1])})
				opener = urllib2.build_opener(proxy_handler)
			else:
				opener = urllib2.build_opener()
		except urllib2.HTTPError as e:
			print('HTTP Error: {0:d} {1:s}'.format(e.code, e.reason), file=sys.stderr)
		except urllib2.URLError as e:
			print('URL Error: {0:s}'.format(e.reason), file = sys.stderr)
			return -1
		except:
			print('Unknow system failure', file = sys.stderr)
			return -1

		while True:
			if failcnt > 3: return -1
			try:
				req = urllib2.Request('http://en.wikipedia.org/w/api.php?' + get_para, headers=header);
				rsp = opener.open(req, timeout=5)

				if rsp.getcode() != 200:
					print('Requesting Wiki fails: {0}'.format(rsp.getcode()), file = sys.stderr)
					failcnt = failcnt + 1
					continue

				data = rsp.read()
				res = json.loads(data)
			except urllib2.HTTPError as e:
				print('HTTP Error: {0:d} {1:s}'.format(e.code, e.reason), file=sys.stderr)
				failcnt = failcnt + 1
				continue
			except urllib2.URLError as e:
				print('URL Error: {0:s}'.format(e.reason), file = sys.stderr)
				failcnt = failcnt + 1
				continue
			except:
				print('Unknow system failure', file = sys.stderr)
				failcnt = failcnt + 1
				continue

			failcnt = 0 #reset fail counter

			for blk in res['query']['backlinks']:
				print('pageid: {0:d}'.format(blk['pageid']))#for debuging
				backlinks.append(blk['pageid'])

			if 'query-continue' in res:
				get_para = urllib.urlencode({
					'action' : 'query',
					'list' : 'backlinks',
					'bllimit' : 'max',
					'blpageid' : pageid,
					'blfilterredir' : 'nonredirects',
					'format' : 'json',
					'bldir' : 'ascending',
					'blcontinue' : res['query-continue']['backlinks']['blcontinue'],
					})
			else:
				break

		return [backlinks]

	def test_phrase_and_get_link(self, *words):
		'''
		@retval [origin_phrase, normalized_phrase, redirect_name, length, backlinks]
		'''
		ret = self.get_longest_phrase(*words)

		if ret[0] <= 0:#can't find any phrase
			retrun -1

		lnks = self.get_links(ret[1][0])
		return [ret[1], ret[2][1], ret[2][2], ret[0], lnks];
