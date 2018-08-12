import json
import sys
import csv
from rdflib import Graph
from rdflib import URIRef
import urllib, json
import argparse


def parse_args(args=sys.argv[1:]):
    """ Get the parsed arguments specified on this script.
    """
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        'endpoint_path',
        action='store',
        type=str,
        help='URL of omeka api endpoint.')

    parser.add_argument(
        'input_path',
        action='store',
        type=str,
        help='Ful path to csv file of ids.')

    parser.add_argument(
        'property_id',
        action='store',
        type=str,
        help='Property id of identifier.')

    return parser.parse_args(args)


if __name__ == "__main__":
    args = parse_args()

    input_path = args.input_path;

    property_id = args.property_id; #10, 98

    mode = ""

    outputPath = input_path+".rdf"

    g = Graph()

    ids = []

    with open(input_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # ヘッダーを読み飛ばしたい時

        for row in reader:

            id = row[0]
            ids.append(id)

    for i in range(0, len(ids)):
        id = ids[i]
        if i % 10 == 0:
            print(str(i)+"/"+str(len(ids))+"\t"+id)

        url = args.endpoint_path+"/items?property%5B0%5D%5Bproperty%5D="+property_id+"&property%5B0%5D%5Btype%5D=eq&property%5B0%5D%5Btext%5D="+id

        try:
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
        except:
            print("Error:\t"+url)


    f2 = open(outputPath, "wb")
    f2.write(g.serialize(format='xml'))
    f2.close()

    print("outputPath:\t"+outputPath)
