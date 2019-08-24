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

import yaml

config_path = "/Users/nakamura/git/min_a/lda/src/data/config.yml"
f = open(config_path, "r+")
config = yaml.load(f)

prefix2 = config["prefix"]

collection_uri = prefix2+"/data/collection.json"
prefix = prefix2+"/data/"
odir = config["doc_dir"]+"/data/"

####

opath = config["src_dir"]+"/logs/thumbnails.xlsx"
files = glob.glob(odir+"manifest/*.json")

rows = []
rows.append(["ID", "Thumbnail"])

for file in files:

    with open(file) as f:
        df = json.load(f)

    subject = df["seeAlso"]
    thumbnail = df["thumbnail"]["@id"] if "thumbnail" in df else ""

    row = [subject, thumbnail]
    rows.append(row)

df = pd.DataFrame(rows)

df.to_excel(opath, index=False, header=False)
