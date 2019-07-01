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

files = glob.glob("data/yanesen/*.xlsx")


df2 = []
df2.append(["item_id", "img_jpeg"])

for file in files:

    print(file)

    df = pd.read_excel(file, sheet_name=0, header=None, index_col=None)

    r_count = len(df.index)
    c_count = len(df.columns)

    for j in range(1, r_count):
        row = []
        for i in range(0, c_count):
            row.append(df.iloc[j, i])
        df2.append(row)

df = pd.DataFrame(df2)

df.to_excel("../data/yanesen.xlsx", index=False, header=False)