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


def parse_args(args=sys.argv[1:]):
    """ Get the parsed arguments specified on this script.
    """
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        'path',
        action='store',
        type=str,
        help='Ful path.')

    return parser.parse_args(args)


args = parse_args()

path = args.path


opath = "../docs/data/metadata.xlsx"

df = pd.read_excel(path, sheet_name=0, header=None, index_col=None)

r_count = len(df.index)
c_count = len(df.columns)

map = {}

for i in range(1, c_count):
    label = df.iloc[0, i]
    uri = df.iloc[1, i]
    type = df.iloc[2, i]

    if not pd.isnull(type):
        obj = {}
        map[i] = obj
        obj["label"] = label
        obj["uri"] = uri
        obj["type"] = type

result = []
row0 = []
row1 = []
for i in map:
    obj = map[i]
    row0.append(obj["label"])
    row1.append(obj["uri"])

'''
row0.append("SeeAlso")
row0.append("IIIF Manifest")
row0.append("Relation")

row1.append("rdfs:seeAlso")
row1.append("dcterms:identifier")
row1.append("dcterms:relation")
'''

result.append(row0)
result.append(row1)

for j in range(3, r_count):
    subject = df.iloc[j, 0]
    row = []
    result.append(row)
    for i in map:
        value = df.iloc[j, i]
        row.append(value)

    '''    
    row.append(subject)

    manifest = subject.replace("/json/", "/manifest/")
    row.append(manifest)

    relation = "https://nakamura196.github.io/uv/?manifest="+manifest
    row.append(relation)
    '''


df = pd.DataFrame(result)

df.to_excel(opath, index=False, header=False)
