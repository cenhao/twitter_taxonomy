#!/usr/bin/env python

from __future__ import print_function
import os, sys, json, codecs, subprocess, re
import happyfuntokenizing
import configReader
import wikiEngine

if len(sys.argv) < 2:
	print("Usage: {:s} <configure_file_path>".format(sys.argv[0]), file = sys.stderr)
	exit(-1)

cfg_reader = configReader.configReader(sys.argv[1])
ret = cfg_reader.loadConfig()

if ret != 0:
	print("Configure file invalid", file = sys.stderr)
	exit(-1)

wiki = wikiEngine.wikiEngine()
ret = wiki._get_longest_phrase("peoples", "republic", "of", "china")

if type(ret) is int:
	print('Get longest phrase fail: {}'.format(ret))
else:
	print('Longest phrase: {}, normalized: {}, pageid: {}'.format(ret[0], ret[1], ret[2]))
