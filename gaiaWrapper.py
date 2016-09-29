#!/usr/bin/python
#
# Author	Yann Bayle
# E-mail	bayle.yann@live.fr
# License   MIT
# Created	19/09/2016
# Updated	29/09/2016
# Version	2
# Object	Wrapper to use Gaia classification
# 			Uses files containing extracted features from Essentia
# Uses  	python gaiaWrapper.py data
# TODOs		Error from gaia: zero division in tonal.chord_progression cf
#			https://github.com/MTG/gaia/issues/47
#

import os
os.system("export PYTHONPATH=/usr/local/lib/python2.7/site-packages:/usr/local/lib/python2.7/site-packages/gaia2:/usr/local/lib/python2.7/site-packages/gaia2/scripts/classification")
import sys
import json_to_sig
import train_model_from_sigs
from contextlib import contextmanager

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout

filesDir = sys.argv[1]
extension = ".essentia"
print("Converting files")
for dirName, subdirList, fileList in os.walk(filesDir):
	for fname in fileList:
		if fname.endswith(extension):
			filelist_file = os.path.join(dirName, fname)
			result_filelist_file = os.path.join(dirName, fname[:-len(extension)] +  ".json")
			with suppress_stdout():
				json_to_sig.convertJsonToSig(filelist_file, result_filelist_file)
print("Training model")
train_model_from_sigs.main(filesDir, None)
