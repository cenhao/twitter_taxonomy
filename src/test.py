from __future__ import print_function
import threading
import wikiEngine2
import sys

'''
thread_local = threading.local()
thread_local.a = 1

def foo():
	#thread_local.a = 2
	print("inside sub-thread: a = {}".format(thread_local.a))

thr = threading.Thread(target=foo)
thr.start()
thr.join()

print("outside subthread: a = {}".format(thread_local.a))
'''

'''
@lru.lru_cache(maxsize = 100)
def foo(num, ref):
	print("go {}".format(num))
	return num + 1

a = [1, 2]

print("{}".format(foo(1, a)))
a[1] = 3
print("{}".format(foo(1, a)))
print("{}".format(foo(1, a)))
print("{}".format(foo(1, a)))
print("{}".format(foo(2, a)))
print("{}".format(foo.__wrapped__(1, a)))

for i in range(1, 10, 1):
	print("{}".format(i))
'''

wiki = wikiEngine2.wikiEngine2()
wiki.set_proxy(sys.argv[1], int(sys.argv[2]))
ret = wiki.get_longest_phrase("NBA")
if isinstance(ret, int):
	print("fail")
	quit()
elif ret[0] <= 0:
	print("no such entry")
else:
	print("len = {0}, phrase = {1}, red = {2}".format(ret[0], ret[1], ret[2][2]))

'''
pageid = ret[2][0]
ret = wiki.get_links(pageid)
for pageid in ret[0]:
	print(pageid)
'''
