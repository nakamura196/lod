# -*- coding: utf-8 -*-
import json
import sys
import csv
from rdflib import Graph
from rdflib import URIRef
import urllib, json

prefix = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/api/items?page="

flg = True
page = 1


obj = dict()
obj["@context"] = "http://iiif.io/api/presentation/2/context.json"
obj["@id"] = "https://nakamura196.github.io/lod/universe.json"
obj["@type"] = "sc:Collection"
manifests = []
obj["manifests"] = manifests

fw = open('universe.json','w')

while flg:

    print(page)

    url = prefix+str(page)

    response = urllib.request.urlopen(url)
    response_body = response.read().decode("utf-8")
    data = json.loads(response_body.split('\n')[0])

    if len(data) > 0:
        for i in range(0, len(data)):
            item = data[i]
            title = item["dcterms:title"][0]["@value"]
            id = item["o:id"]
            manifest_uri = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/"+str(id)+"/manifest"

            obj2 = dict()
            manifests.append(obj2)
            obj2["@id"] = manifest_uri
            obj2["@type"] = "sc:Manifest"
            obj2["label"] = title

    else:
        flg = False

    page += 1

#ココ重要！！
# json.dump関数でファイルに書き込む
json.dump(obj,fw)
