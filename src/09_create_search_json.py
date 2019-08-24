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

collection_uri = "https://nakamura196.github.io/lda/data/collection.json"

prefix = "https://nakamura196.github.io/lda/data/"
odir = "../docs/data/"

response = urllib.request.urlopen(collection_uri)
collection = json.loads(response.read().decode('utf8'))

manifests = collection["manifests"]
result = {}


data = []
result["rows"] = data

config  = {
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
    "aggregations": {
        "test": {
            "title": 'Tags',
            "size": 10
        }
    }
}
result["config"] = config

config["searchableFields"].append("label")
config["searchableFields"].append("description")

for i in range(len(manifests)):

    m = str(i % 2)

    manifest_uri = manifests[i]["@id"]
    
    print(str(i+1)+"/"+str(len(manifests)))


    # response = urllib.request.urlopen(manifest_uri)
    # manifest = json.loads(response.read().decode('utf8'))

    # jsonファイルを読み込む
    f = open(manifest_uri.replace(prefix, odir))
    # jsonデータを読み込んだファイルオブジェクトからPythonデータを作成
    manifest = json.load(f)
    # ファイルを閉じる
    f.close()

    obj = {
        "label" : manifest["label"],
        "related" : manifest["relation"],
        "thumbnail" : manifest["thumbnail"]["@id"]
    }

    manifest["metadata"] = [
        {
            "label" : "a",
            "value": manifest["label"][0:1]
        },
        {
            "label": "a",
            "value": manifest["label"][1:2]
        }
    ]

    obj["test"] = [m]
    obj["description"] = "aaaaaaaaaaaa"+str(m)

    for metadata in manifest["metadata"]:
        label = metadata["label"]
        value = metadata["value"]

        if label not in config["aggregations"]:
            config["aggregations"][label] = {
                "title": label,
                "size": 10
            }

            config["searchableFields"].append(label)

        if label not in obj:
            obj[label] = []

        obj[label].append(value)

        # obj[label] = [value]

    data.append(obj)



f2 = open(collection_uri.replace(prefix, odir).replace("collection.json", "items.json"), 'w')
json.dump(result, f2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))
