import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
import pandas as pd
import json
import urllib.request
import os
from PIL import Image
import glob
import shutil
import yaml

config_path = "/Users/nakamura/git/min_a/lda/src/data/config.yml"
f = open(config_path, "r+")
config = yaml.load(f)

doc_dir = config["doc_dir"]
src_dir = config["src_dir"]

prefix = config["prefix"]


f = open(src_dir+'/tmp/convert.sh', 'w')
writer = csv.writer(f, lineterminator='\n')


files = glob.glob(
    doc_dir+'/data/image/original/**/*.jpg', recursive=True)
for file in files:

    base_dir = file.replace(".jpg", "")
    odir = base_dir.replace("/original/", "/tile/")

    sym_link_path = odir+"/full/full/0/default.jpg"

    os.makedirs(os.path.split(sym_link_path)[0], exist_ok=True)

    # os.symlink(file, sym_link_path)
    os.unlink(sym_link_path)

    shutil.copyfile(file, sym_link_path)

f.close()
