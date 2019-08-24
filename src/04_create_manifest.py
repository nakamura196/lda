import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
import pandas as pd
import json
import urllib.request
import os
from PIL import Image

path_metadata = "/Users/nakamura/git/lda/src/data/yanesen-01_10.xlsx"
path_image = "/Users/nakamura/git/lda/src/data/yanesen_images.xlsx"


def get_id_image_map():
    df = pd.read_excel(path_image, sheet_name=0,
                       header=None, index_col=None)

    map = {}

    r_count = len(df.index)
    c_count = len(df.columns)

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

viewingDirection = "right-to-left"
logo = "https://nakamura196.github.io/lda/assets/images/favicon.ico"
within = "https://nakamura196.github.io/lda/"
attribution = "地域文化資源デジタルアーカイブ"
license = "http://creativecommons.org/licenses/by/4.0/"

prefix = "https://nakamura196.github.io/lda/data/manifest/"
odir = "/Users/nakamura/git/lda/docs/data/manifest/"

id_image_map = get_id_image_map()

for j in range(3, r_count):

    seeAlso = df.iloc[j, 0]

    id = df.iloc[j, 1]

    manifest_uri = seeAlso.replace("/json/", "/manifest/")

    relation = "https://nakamura196.github.io/uv/?manifest="+manifest_uri

    title = df.iloc[j, 2]

    manifest = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@type": "sc:Manifest",
        "@id": manifest_uri,
        "license": license,
        "attribution": attribution,
        "label": title,
        "logo": logo,
        "within": within,
        "viewingDirection": viewingDirection,
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

    canvases = manifest["sequences"][0]["canvases"]

    images = id_image_map[id]
    for i in range(len(images)):

        img_url = images[i]

        if i == 0:
            manifest["thumbnail"] = {
                "@id" : img_url
            }

        canvas_id = manifest_uri+"/canvas/p"+str(i+1)

        canvas_label = "["+str(i+1)+"]"

        img = Image.open(urllib.request.urlopen(img_url))
        width, height = img.size

        canvas = {
            "@type": "sc:Canvas",
            "@id": canvas_id,
            "label": canvas_label,
            "thumbnail": {
                "@id" : img_url
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
                        "@id": img_url
                    },
                    "on": canvas_id
                }
            ],
            "width": width,
            "height": height
        }

        canvases.append(canvas)



    f2 = open(manifest_uri.replace(prefix, odir), 'w')
    json.dump(manifest, f2, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))
