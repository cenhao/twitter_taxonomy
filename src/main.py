#!/usr/bin/env python

from __future__ import print_function
import os, sys, json, codecs, subprocess, re
import happyfuntokenizing
import configReader
import wikiEngine2
import thread_run
import Queue
import threading

if len(sys.argv) < 2:
	print("Usage: {:s} <configure_file_path>".format(sys.argv[0]), file = sys.stderr)
	exit(-1)

#sys.stdout = codecs.getwriter('utf-8')(sys.__stdout__) 
cfg_reader = configReader.configReader(sys.argv[1])
ret = cfg_reader.load_config()

if ret != 0:
	print("Configure file invalid", file = sys.stderr)
	exit(-1)

wiki = wikiEngine2.wikiEngine2()
job_queue = Queue.Queue(cfg_reader.get_proxy_num())
fail_queue = Queue.Queue()
ts = []

for i in range(0, cfg_reader.get_proxy_num()):
	ts.append(threading.Thread(target=thread_run.thread_run, args=(wiki, cfg_reader.get_proxy(i)[0], cfg_reader.get_proxy(i)[1],
		cfg_reader.max_phrase_length(), job_queue, fail_queue)))
	ts[-1].start()

line_cnt = 0

with open(cfg_reader.raw_data_path()) as fp:
	for line in fp:
		while not fail_queue.empty():
			job_queue.put(fail_queue.get())

		line_cnt = line_cnt + 1
		job_queue.put([line_cnt, line])

while not fail_queue.empty():
	job_queue.put(fail_queue.get())

for i in xrange(0, cfg_reader.get_proxy_num()):
	job_queue.put(i)

for i in xrange(0, cfg_reader.get_proxy_num()):
	ts[i].join()
