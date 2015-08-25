#!/bin/python

import os
import hashlib
import pickle

os.chdir ('./SNC_folder')
filelist = []
for i in [k for asd,asdf,k in os.walk('.')][0]: filelist.append(os.getcwd() + '/' + i)
digest = {}
for i in filelist: digest[str(hashlib.md5(open(i).read(128)).hexdigest())] = i
