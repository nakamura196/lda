import csv
import cv2
import numpy as np
import glob
import json
import urllib.request
import tempfile
import requests
import requests
import shutil

f = open("curation.json", 'r')

#ココ重要！！
json_data = json.load(f)  # JSON形式で読み込む

selection = json_data["selections"][0]
members = selection["members"]
manifest = selection["within"]["@id"]

res = urllib.request.urlopen(manifest)
data = json.loads(res.read())

canvas_image_map = {}

canvases = data["sequences"][0]["canvases"]
for i in range(len(canvases)):
    canvas = canvases[i]
    canvas_id = canvas["@id"]
    image_url = canvas["images"][0]["resource"]["service"]["@id"]
    canvas_image_map[canvas_id] = image_url


f = open('some.csv', 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerow(["relation", "r", "c", "thumbnail"])



for i in range(len(members)):
    
    member = members[i]
    relation = "http://codh.rois.ac.jp/software/iiif-curation-viewer/demo/?curation=https://raw.githubusercontent.com/nakamura196/nagai/master/docs/data/curation/aaa.json&pos="+str(i+1)
    text = member["label"].split("-")
    r = int(text[0])
    c = int(text[1])

    id = member["@id"].split("#xywh=")
    canvas_id = id[0]
    thumbnail = canvas_image_map[canvas_id]+"/"+id[1]+"/200,/0/default.jpg"

    row = [relation, r, c, thumbnail]
    writer.writerow(row)

f.close()
