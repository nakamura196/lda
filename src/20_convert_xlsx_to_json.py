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


prefix = config["prefix"]
odir = config["doc_dir"]
path_metadata = config["src_dir"] + "/data/metadata.xlsx"
opath = odir + "/data/data.json"


df = pd.read_excel(path_metadata, sheet_name=0, header=None, index_col=None)

r_count = len(df.index)
c_count = len(df.columns)

map = {}

for i in range(0, c_count):
    label = df.iloc[0, i]
    uri = df.iloc[1, i]
    type = df.iloc[2, i]

    if not pd.isnull(type):
        obj = {}
        map[i] = obj
        obj["label"] = label
        obj["uri"] = uri
        obj["type"] = type

g2 = Graph()

for j in range(4, r_count):

    g = Graph()

    subject_str = df.iloc[j,0]
    subject = URIRef(subject_str)
    for i in map:
        value = df.iloc[j,i]

        if not pd.isnull(value) and value != 0:

            obj = map[i]
            p = URIRef(obj["uri"])

            if obj["type"].upper() == "RESOURCE":
                g.add((subject, p, URIRef(value)))
                g2.add((subject, p, URIRef(value)))
            else:
                g.add((subject, p, Literal(value)))
                g2.add((subject, p, Literal(value)))

    g.serialize(subject_str.replace(prefix, odir), format='json-ld')

g2.serialize(opath, format='json-ld')
