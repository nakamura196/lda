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

odir = "/Users/nakamura/git/lda/docs/data/"

opath = "data/thumbnails.xlsx"
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
