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

collection_uri = "https://archdataset.dl.itc.u-tokyo.ac.jp/collections/fujikawa/image/collection.json"

odir = "tmp"

size = 10

response = urllib.request.urlopen(collection_uri)
collection = json.loads(response.read().decode('utf8'))

manifests = collection["manifests"]
result = {}
aggregations = {}
aggregations2 = {}

data = []
result["rows"] = data

config = {
    "searchableFields": [],
    "sortings": {
        "label_asc": {
            "field": 'label',
            "order": 'asc'
        },
        "label_desc": {
            "field": 'label',
            "order": 'desc'
        }
    },
    "aggregations": aggregations2
}
result["config"] = config

config["searchableFields"].append("label")
config["searchableFields"].append("description")
config["searchableFields"].append("fulltext")

for i in range(len(manifests)):

    manifest_uri = manifests[i]["@id"]

    print(str(i+1)+"/"+str(len(manifests)))

    response = urllib.request.urlopen(manifest_uri)
    manifest = json.loads(response.read().decode('utf8'))

    thumbnail = None
    if "thumbnail" in manifest:
        if "@id" in manifest["thumbnail"]:
            thumbnail = manifest["thumbnail"]["@id"]
        else:
            thumbnail = manifest["thumbnail"]

    fulltext = ""

    obj = {
        "label": manifest["label"],
        "related": manifest["related"]
    }

    obj["thumbnail"] = thumbnail

    if "description" in manifest:
        obj["description"] = manifest["description"]

    for metadata in manifest["metadata"]:
        label = metadata["label"]
        value = metadata["value"]

        if isinstance(value, list):
            values = value
        else:
            values = [value]

        for value in values:

            if "http" not in value:

                if label not in aggregations:
                    aggregations[label] = {
                        "title": label,
                        "map" : {}
                    }

                if label not in obj:
                    obj[label] = []

                map = aggregations[label]["map"]

                if value not in map:
                    map[value] = 0

                map[value] = map[value] + 1

                obj[label].append(value)
                fulltext += " "+value

    obj["fulltext"] = fulltext
    data.append(obj)

for field in aggregations:
    obj = aggregations[field]
    map = obj["map"]
    map = sorted(map.items(), key=lambda kv: kv[1], reverse=True)

    if map[0][1] > 1 and len(map) != 1:
        aggregations2[field] = {
            "title": obj["title"],
            "size": size
        }

f2 = open(odir+"/items.json", 'w')
json.dump(result, f2, ensure_ascii = False, indent = 4,
            sort_keys = True, separators = (',', ': '))
