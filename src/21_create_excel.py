import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
import pandas as pd
import json
import urllib.request
import os
from PIL import Image


import pandas as pd
from rdflib import URIRef, BNode, Literal, Graph
from rdflib.namespace import RDF, RDFS, FOAF, XSD
from rdflib import Namespace
import numpy as np
import math
import sys
import argparse
import json

import yaml


def parse_args(args=sys.argv[1:]):
    """ Get the parsed arguments specified on this script.
    """
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        'config_path',
        action='store',
        type=str,
        help='config path.')

    return parser.parse_args(args)


args = parse_args()

config_path = args.config_path
f = open(config_path, "r+")
config = yaml.load(f)

odir = config["doc_dir"]
path_metadata = config["src_dir"] + "/data/metadata.xlsx"
opath = odir + "/data/data.xlsx"

df = pd.read_excel(path_metadata, sheet_name=0, header=None, index_col=None)

r_count = len(df.index)
c_count = len(df.columns)

map = {}

for i in range(0, c_count):
    label = df.iloc[0, i]
    uri = df.iloc[1, i]
    type = df.iloc[2, i]
    target = df.iloc[3, i]

    if not pd.isnull(target) and target == "metadata":
        obj = {}
        map[i] = obj
        obj["label"] = label

    if uri == "http://purl.org/dc/terms/relation":
        relation_index = i

result = []
row0 = []
for i in map:
    obj = map[i]
    row0.append(obj["label"])

row0.append("relation")

result.append(row0)

for j in range(4, r_count):
    row = []
    result.append(row)
    for i in map:
        value = df.iloc[j, i]
        row.append(value)
    row.append(df.iloc[j, relation_index])


df = pd.DataFrame(result)

df.to_excel(opath, index=False, header=False)
