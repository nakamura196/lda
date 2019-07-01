import cv2
import numpy as np
import glob
import json
import urllib.request
import tempfile
import requests
import requests
import shutil

manifest = "https://diyhistory.org/public/omekas13/iiif/1/manifest"

res = urllib.request.urlopen(manifest)
data = json.loads(res.read())

canvases = data["sequences"][0]["canvases"]

f = open("edit.json", 'r')

#ココ重要！！
json_data = json.load(f)  # JSON形式で読み込む

arr = {}

for obj in json_data["@graph"]:
    id = obj["target"]["id"].split("#xywh=")
    image_url = id[0]
    if image_url not in arr:
        arr[image_url] = []

    text = obj["bodyValue"].split("-")

    r = text[0].zfill(3)
    c = text[1].zfill(3)

    text = r + "-" + c

    obj2 = {
        "text": text,
        "area": id[1]
    }
    arr[image_url].append(obj2)

print(arr)

curation = {
    "@context": [
        "http://iiif.io/api/presentation/2/context.json",
        "http://codh.rois.ac.jp/iiif/curation/1/context.json"
    ],
    "@type": "cr:Curation",
    "@id": "http://mp.ex.nii.ac.jp/api/curation/json/dadfe3f0-d765-4da7-8930-75728b94d318",
    "label": "Curating list",
    "selections": [
        {
            "@id": "http://mp.ex.nii.ac.jp/api/curation/json/dadfe3f0-d765-4da7-8930-75728b94d318/range1",
            "@type": "sc:Range",
            "label": "Manual curation by IIIF Curation Viewer",
            "members": [
                
            ],
            "within": {
                "@id": "https://free.iiifhosting.com/iiif/539ddf753eb35a12696c4fde4d5c9156330c796e79c5402ed8a8b2f0aff8b208/manifest.json",
                "@type": "sc:Manifest",
                "label": "iiif/539ddf753eb35a12696c4fde4d5c9156330c796e79c5402ed8a8b2f0aff8b208"
            }
        }
    ]
}

curation["@id"] = "https://nakamura196.github.io/nagai/data/curation/"+"aaa"+".json"

selection = curation["selections"][0]

selection["@id"] = curation["@id"]+"/range1"

within = selection["within"]
within["@id"] = manifest
within["label"] = data["label"]

members = selection["members"]


for i in range(len(canvases)):
    canvas = canvases[i]
    canvas_id = canvas["@id"]
    image_url = canvas["images"][0]["resource"]["@id"]

    anno_list = arr[image_url]

    anno_list.sort(key=lambda x: x['text'])

    for anno in anno_list:
        
        member = {
            "@id": "http://free.iiifhosting.com/iiif/539ddf753eb35a12696c4fde4d5c9156330c796e79c5402ed8a8b2f0aff8b208/can0.json#xywh=1656,1684,312,452",
            "@type": "sc:Canvas",
            "label": "iiif/539ddf753eb35a12696c4fde4d5c9156330c796e79c5402ed8a8b2f0aff8b208 - image 0"
        }

        member["@id"] = canvas_id+"#xywh="+anno["area"]
        member["label"] = anno["text"]
        members.append(member)

fw = open("curation.json", 'w')
json.dump(curation, fw, ensure_ascii=False, indent=4,
          sort_keys=True, separators=(',', ': '))
