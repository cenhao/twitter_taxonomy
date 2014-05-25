#!/usr/bin/env python

from __future__ import print_function
import os, sys, json, codecs, subprocess, re
import happyfuntokenizing
import configReader
import wikiEngine

if len(sys.argv) < 2:
	print("Usage: {:s} <configure_file_path>".format(sys.argv[0]), file = sys.stderr)
	exit(-1)

#sys.stdout = codecs.getwriter('utf-8')(sys.__stdout__) 
cfg_reader = configReader.configReader(sys.argv[1])
ret = cfg_reader.loadConfig()

if ret != 0:
	print("Configure file invalid", file = sys.stderr)
	exit(-1)

wiki = wikiEngine.wikiEngine()
#ret = wiki.getLinks("peoples", "republic", "of", "china")
ret = wiki.getLinks("japan")
#ret = wiki._get_longest_phrase("peoples", "republic", "of", "china")
