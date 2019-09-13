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

files = glob.glob(odir+"manifest/*.json")

manifests = []

for file in files:

    

    try:

        with open(file) as f:
            df = json.load(f)

        manifest = {
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": df["@id"],
            "@type": "sc:Manifest",
            "label": df["label"]
        }

        if "thumbnail" in df:
            manifest["thumbnail"] = df["thumbnail"]["@id"]

        manifests.append(manifest)
    except:
        print("Error: "+file)

collection = {
    "@context": "http://iiif.io/api/presentation/2/context.json",
    "@id": collection_uri,
    "@type": "sc:Collection",
    "label": "谷根千デジタルアーカイブ",
    "vhint": "use-thumb",
    "manifests": manifests
}


f2 = open(collection_uri.replace(prefix, odir), 'w')
json.dump(collection, f2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))
