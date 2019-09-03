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

files = glob.glob(
    doc_dir+'/data/image/original/**/*.jpg', recursive=True)

for file in files:
    print(file)

    img = Image.open(file, 'r')
    width, height = img.size
    if width > height:
        thumbnail_size = (200, height * 200 / width)
    else:
        thumbnail_size = (width * 200 / height, 200)
    img.thumbnail(thumbnail_size)
    opath = file.replace("/original/", "/medium/")
    tmp = os.path.split(opath)
    os.makedirs(tmp[0], exist_ok=True)
    img.save(file.replace("/original/", "/medium/"), 'JPEG')
