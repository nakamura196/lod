import json
import sys
import csv
from rdflib import Graph
from rdflib import URIRef
import urllib, json

argvs = sys.argv  # コマンドライン引数を格納したリストの取得
argc = len(argvs) # 引数の個数

if (argc < 2):   # 引数が足りない場合は、その旨を表示
    print('Usage: # python %s filename' % argvs[0])
    quit()         # プログラムの終了


inputPath = argvs[1];

mode = ""
if argc == 3:
    mode = argvs[2]

outputPath = inputPath+".rdf"

prefix = "https://iiif.dl.itc.u-tokyo.ac.jp/repo"

g = Graph()

ids = []

with open(inputPath, 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    for row in reader:

        id = row[0]
        ids.append(id)

for i in range(0, len(ids)):
    id = ids[i]
    if i % 10 == 0:
        print(str(i)+"/"+str(len(ids))+"\t"+id)

    url = prefix+"/api/items?search="+id

    response = urllib.request.urlopen(url)
    response_body = response.read().decode("utf-8")
    data = json.loads(response_body.split('\n')[0])

    if len(data) == 1:
        data = data[0]

        iri = data["@id"]

        try:
            g2 = Graph()
            g2.parse(iri, format="json-ld")
            g2.serialize(format='xml')
            g.parse(iri, format="json-ld")

        except:
            import traceback
            traceback.print_exc()


    if mode == "test":
        if i > 5:
            break


f2 = open(outputPath, "wb")
f2.write(g.serialize(format='xml'))
f2.close()

print("outputPath:\t"+outputPath)
