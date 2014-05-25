from __future__ import print_function
import lru

@lru.lru_cache(maxsize = 100)
def foo(num):
	print("go {}".format(num))
	return num + 1

print("{}".format(foo(1)))
print("{}".format(foo(1)))
print("{}".format(foo(1)))
print("{}".format(foo(1)))
print("{}".format(foo(2)))
print("{}".format(foo.__wrapped__(1)))

for i in range(1, 10, 1):
	print("{}".format(i))

l = [2, 3, 4]
print(len([1, *l]))
