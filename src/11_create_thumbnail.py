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

files = glob.glob(
    '/Users/nakamura/git/min_a/lda/docs/data/image/original/**/*.jpg', recursive=True)
for file in files:
    print(file)

    img = Image.open(file, 'r')
    width, height = img.size
    if width > height:
        thumbnail_size = (200, height * 200 / width)
    else:
         thumbnail_size = (width * 200 / height,200)
    img.thumbnail(thumbnail_size)
    opath = file.replace("/original/", "/medium/")
    tmp = os.path.split(opath)
    os.makedirs(tmp[0], exist_ok=True)
    img.save(file.replace("/original/", "/medium/"), 'JPEG')

'''
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
'''
