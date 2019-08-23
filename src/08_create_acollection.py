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

collection_uri = "https://nakamura196.github.io/lda/data/acollection.json"
prefix = "https://nakamura196.github.io/lda/data/"
odir = "../docs/data/"

files = glob.glob(odir+"image/iiif/*/manifest.json")

manifests = []

for file in files:

    with open(file) as f:
        df = json.load(f)

    manifest = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": file.replace(odir, prefix),
        "@type": "sc:Manifest",
        "label": df["label"]
    }

    if "thumbnail" in df:
        manifest["thumbnail"] = df["thumbnail"]["@id"]

    manifests.append(manifest)

collection = {
    "@context": "http://iiif.io/api/presentation/2/context.json",
    "@id": "https://nakamura196.github.io/lda/data/acollection.json",
    "@type": "sc:Collection",
    "label": "IIIF Collection",
    "vhint": "use-thumb",
    "manifests": manifests
}


f2 = open(collection_uri.replace(prefix, odir), 'w')
json.dump(collection, f2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))
