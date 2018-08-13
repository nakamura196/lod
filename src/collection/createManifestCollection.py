from SPARQLWrapper import SPARQLWrapper
import json

sparql = SPARQLWrapper(endpoint='https://dydra.com/ut-digital-archives/lod/sparql', returnFormat='json')
sparql.setQuery("""
    PREFIX uterms:  <http://purl.org/utrepo/terms#>
    PREFIX o:  <http://omeka.org/s/vocabs/o#>
    SELECT * WHERE {
    ?s uterms:manifestUri ?manifestUri .
    ?s dcterms:title ?label .
    ?s dcterms:rights ?license .
    ?s o:id ?id .
    } order by ?id
""")
results = sparql.query().convert()

collection = {}
collection["@context"] = "http://iiif.io/api/presentation/2/context.json"
collection["@id"] = "https://nakamura196.github.io/lod/collection/collection.json"
collection["@type"] = "sc:Collection"
collection["label"] = "IIIF Collections from UTokyo Digital Archives Project"

manifests = []
collection["manifests"] = manifests

for obj in results["results"]["bindings"]:
    manifest = {}
    print(obj)
    manifest["@id"] = obj["manifestUri"]["value"]
    manifest["@type"] = "sc:Manifest"
    manifest["label"] = obj["label"]["value"]
    manifest["license"] = obj["license"]["value"]

    manifests.append(manifest)

fw = open("../../docs/collection/collection.json",'w')
json.dump(collection, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
