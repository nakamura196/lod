from SPARQLWrapper import SPARQLWrapper
import json
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import pandas as pd
import openpyxl

sparql = SPARQLWrapper(endpoint='https://dydra.com/ut-digital-archives/lod/sparql', returnFormat='json')
sparql.setQuery("""
    PREFIX o:  <http://omeka.org/s/vocabs/o#>
    PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT * WHERE {
    ?s rdf:type o:Item .
    ?s o:id ?id .
    ?s ?v ?o .
    } order by ?id
""")

prefixes = {}
prefixes["http://iiif.io/api/presentation/2#"] = "sc"
prefixes["http://purl.org/utrepo/terms#"] = "uterms"
prefixes["http://data.archiveshub.ac.uk/def/"] = "archiveshub"
prefixes["http://purl.org/dc/terms/"] = "dcterms"
prefixes["http://ndl.go.jp/dcndl/terms/"] = "dcndl"
prefixes["http://www.w3.org/2000/01/rdf-schema#"] = "rdfs"
prefixes["http://purl.org/ontology/bibo/"] = "bibo"
prefixes["http://www.w3.org/1999/02/22-rdf-syntax-ns#"] = "rdf"
prefixes["http://xmlns.com/foaf/0.1/"] = "foaf"

results = sparql.query().convert()

data = {}
fields = []

for obj in results["results"]["bindings"]:

    id = int(obj["id"]["value"])
    s = obj["s"]["value"]
    v = obj["v"]["value"]

    if v.find("http://omeka.org/s/vocabs/o#") != -1:
        continue;
    if v not in fields:
        fields.append(v)

    o = obj["o"]["value"]

    if id not in data:
        data[id] = {}

    map = data[id]

    if v not in map:
        map[v] = []

    map[v].append(o)

table = []

#一行目
row = []
table.append(row)
for key in sorted(fields):
    for prefix in prefixes:
        key = key.replace(prefix, prefixes[prefix]+":")
    row.append(key)

#二行目以降
for id in sorted(data):
    obj = data[id]
    row = []
    table.append(row)
    for v in sorted(fields):
        text = ""
        if v in obj:
            values = obj[v]
            for i in range(len(values)):
                text += obj[v][i]
                if i != len(values) - 1:
                    text += "|"
        row.append(text)

df = pd.DataFrame(table);

df.to_excel('dataset.xlsx', index=False, header=False)
# df.to_csv('dataset.tsv', sep='\t', index=False, header=False)
