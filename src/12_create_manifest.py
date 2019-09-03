import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
import pandas as pd
import json
import urllib.request
import os
from PIL import Image
import yaml
import requests

config_path = "/Users/nakamura/git/min_a/lda/src/data/config.yml"
f = open(config_path, "r+")
config = yaml.load(f)

image_api = config["prefix"]
data_dir = config["src_dir"] +"/data"
path_metadata = data_dir+"/metadata.xlsx"
path_image = data_dir+"/images.xlsx"
manifest_dir = "/data/manifest/"
doc_dir = config["doc_dir"]
odir = doc_dir+ manifest_dir
prefix = image_api + manifest_dir

def get_id_image_map():
    df = pd.read_excel(path_image, sheet_name=0,
                       header=None, index_col=None)

    map = {}

    r_count = len(df.index)

    for j in range(1, r_count):

        id = df.iloc[j, 0]
        image = df.iloc[j, 1]

        if id not in map:
            map[id] = []

        map[id].append(image)

    return map

df = pd.read_excel(path_metadata, sheet_name=0, header=None, index_col=None)

r_count = len(df.index)
c_count = len(df.columns)

'''
viewingDirection = "right-to-left"
logo = "https://nakamura196.github.io/lda/assets/images/favicon.ico"
within = "https://nakamura196.github.io/lda/"
attribution = "地域文化資源デジタルアーカイブ"
license = "http://creativecommons.org/licenses/by/4.0/"
'''

id_image_map = get_id_image_map()

map = {}

for i in range(0, c_count):
    label = df.iloc[0, i]
    uri = df.iloc[1, i]
    # type = df.iloc[2, i]
    target=df.iloc[3,i]

    if target == "metadata":
        obj = {}
        map[i] = obj
        obj["label"] = label

    if uri == "http://purl.org/dc/terms/rights":
        license_index = i
    if uri == "http://purl.org/dc/terms/title":
        title_index = i
    if uri == "http://purl.org/dc/terms/description":
        description_index = i
    if uri == "http://www.w3.org/2000/01/rdf-schema#seeAlso":
        seeAlso_index = i
    if uri == "http://purl.org/dc/terms/identifier":
        identifier_index = i
    if label == "logo":
        logo_index = i
    if label == "attribution":
        attribution_index = i
    if label == "within":
        within_index = i
    if label == "viewingDirection":
        viewingDirection_index = i
    if uri == "http://purl.org/dc/terms/relation":
        related_index = i

    '''
    if not pd.isnull(type):
        obj = {}
        map[i] = obj
        obj["label"] = label
        obj["uri"] = uri
        obj["type"] = type
    '''

for j in range(4, r_count):

    print(str(j)+"/"+str(r_count))

    seeAlso = df.iloc[j, seeAlso_index]

    id = df.iloc[j, identifier_index]

    manifest_uri = seeAlso.replace("/json/", "/manifest/")

    # relation = "http://da.dl.itc.u-tokyo.ac.jp/uv/?manifest="+manifest_uri
    relation = df.iloc[j, related_index]

    title = df.iloc[j, title_index]

    metadata = []
    for index in map:
        value = df.iloc[j, index]
        if not pd.isnull(value) and value != 0:
            values = value.split(",")
            for value in values:
                metadata.append({
                    "label": map[index]["label"],
                    "value" : value.strip()
                })

    manifest = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@type": "sc:Manifest",
        "@id": manifest_uri,
        "license": df.iloc[j, license_index],
        "attribution": df.iloc[j, attribution_index],
        "label": title,
        "logo": df.iloc[j, logo_index],
        "within": df.iloc[j, within_index],
        "viewingDirection": df.iloc[j, viewingDirection_index],
        "seeAlso": seeAlso,
        "related": relation,
        "sequences": [
            {
                "@type": "sc:Sequence",
                "@id": manifest_uri+"/sequence/normal",
                "label": "Current Page Order",
                "viewingHint": "non-paged",
                "canvases": []
            }
        ]
    }

    if len(metadata) > 0:
        manifest["metadata"] = metadata

    if description_index != None:
        value = df.iloc[j, description_index]
        if not pd.isnull(value) and value != 0:
            manifest["description"] = value

    canvases = manifest["sequences"][0]["canvases"]

    images = id_image_map[id]
    for i in range(len(images)):

        img_url = images[i]

        if "info.json" in img_url:

            r = requests.get(img_url)
            info = r.json()

            image_api = img_url.replace("/info.json", "")

            thumbnail = image_api+"/full/"+str(info["sizes"][0]["width"])+",/0/default.jpg"

            width = info["width"]
            height = info["height"]

            service = {
                "@context": info["@context"],
                "@id": image_api,
                "profile": info["profile"][0]
            }

            img_id = image_api+"/full/full/0/default.jpg"

        else:
            thumbnail = img_url.replace("/original/", "/medium/")

            img_path = img_url.replace(image_api, doc_dir)

            img = Image.open(img_path)
            width, height = img.size

            img_id = img_url

        canvas_id = manifest_uri+"/canvas/p"+str(i+1)

        canvas_label = "["+str(i+1)+"]"

        canvas = {
            "@type": "sc:Canvas",
            "@id": canvas_id,
            "label": canvas_label,
            "thumbnail": {
                "@id": thumbnail
            },
            "images": [
                {
                    "@type": "oa:Annotation",
                    "motivation": "sc:painting",
                    "@id": manifest_uri + "/annotation/p"+str(i+1)+"-image",
                    "resource": {
                        "@type": "dctypes:Image",
                        "format": "image/jpeg",
                        "width" : width,
                        "height" : height,
                        "@id": img_id
                    },
                    "on": canvas_id
                }
            ],
            "width": width,
            "height": height
        }

        if i == 0:
            manifest["thumbnail"] = {
                "@id" : thumbnail
            }

        if "info.json" in img_url:
            canvas["thumbnail"]["service"] = service
            canvas["images"][0]["resource"]["service"] = service
            # canvas["images"][0]["resource"]["service"]["width"] = width
            # canvas["images"][0]["resource"]["service"]["height"] = height

        canvases.append(canvas)



    f2 = open(manifest_uri.replace(prefix, odir), 'w')
    json.dump(manifest, f2, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))
