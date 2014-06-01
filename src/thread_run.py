from __future__ import print_function
import sys
import wikiEngine2
import happyfuntokenizing
import threading
import Queue

output_lock = threading.Lock()

def thread_run(wiki, proxy_ip, port, phrase_len, queue, fail_queue):
	ident = threading.current_thread().ident
	if proxy_ip is not None: wiki.set_proxy(proxy_ip, port)
	tok = happyfuntokenizing.Tokenizer(preserve_case=False, no_url=True)
	failcnt = 0

	while True:
		job = queue.get()

		if isinstance(job, int):
			print("thread ends", file=sys.stderr)
			return

		words = map((lambda x : x if x[0] != "#" and x[0] != '@' else x[1:]), tok.tokenize(job[1]))
		#TODO maybe more processing here

		l = len(words)
		phrase_list = []

		i = 0
		fail = False

		while i < l:
			ret = wiki.get_longest_phrase(*words[i:i+phrase_len])

			if isinstance(ret, int):
				failcnt = failcnt + 1
				fail_queue.put(job)
				if failcnt > 30:
					print("thread {0:s} failed more than 30 times in a line, it killed itself".format(threading.current_thread().name), file=sys.stderr)
					return
				fail = True
				break
			else: failcnt = 0

			if ret[0] > 0:#phrase found
				phrase_list.append(ret)
				i = i + ret[0] - 1

			i = i + 1

		if fail: continue
		output_lock.acquire()
		print("{0:d}||{1:d}".format(job[0], len(phrase_list)), end='')

		for i in range(0, len(phrase_list)):
			print("||{0:d}##{1:s}".format(phrase_list[i][2][0], phrase_list[i][2][1]), end='')

		print("")
		output_lock.release()
