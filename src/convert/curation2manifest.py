import glob
import json
import os
import urllib.request

files = glob.glob('/Users/nakamura/git/kunshujo/docs/data/curation/*.json')

# odir = "/Users/nakamura/git/dataset/docs/collections/tanaka/image/anno"
odir = "/Users/nakamura/git/dataset_tmp/docs/collections/tanaka/image/anno"

# prefix = "https://archdataset.dl.itc.u-tokyo.ac.jp/collections/tanaka/image/anno"
prefix = "https://nakamura196.github.io/dataset_tmp/collections/tanaka/image/anno"

result = {}

for file in files:

    with open(file, 'r') as f:
        obj = json.load(f)

    selections = obj["selections"]

    for selection in selections:

        members = selection["members"]
        within = selection["within"]
        manifest = within["@id"]

        if manifest not in result:
            result[manifest] = {}

        manifest_obj = result[manifest]

        for member in members:
            id = member["@id"]
            tmp = id.split("#")
            canvas_id = tmp[0]
            area = tmp[1]

            if canvas_id not in manifest_obj:
                manifest_obj[canvas_id] = {}

            canvas_obj = manifest_obj[canvas_id]
            canvas_obj[area] = member["metadata"]

for manifest in result:

    print(manifest)

    manifest_obj = result[manifest]

    id = manifest.split("/")[5]

    dir = odir + "/" + id
    os.makedirs(dir, exist_ok=True)

    res = urllib.request.urlopen(manifest)
    # json_loads() でPythonオブジェクトに変換
    data = json.loads(res.read().decode('utf-8'))

    # print(data)

    canvases = data["sequences"][0]["canvases"]

    for i in range(len(canvases)):
        canvas = canvases[i]
        canvas_id = canvas["@id"]

        canvas["label"] = {
            "@value": canvas["label"]
        }

        if canvas_id in manifest_obj:

            anno_filename = "p"+str(i+1).zfill(4)+"-annolist.json"

            annotation_url = prefix + "/" + id + "/" + anno_filename

            canvas["otherContent"] = [
                {
                    "@id": annotation_url,
                    "@type": "sc:AnnotationList"
                }
            ]

            annotationlist = {
                "@context": "http://iiif.io/api/presentation/2/context.json",
                "@id": annotation_url,
                "@type": "sc:AnnotationList",
                "resources": [

                ]
            }

            count = 1

            curation = manifest_obj[canvas_id]

            for area in curation:

                text = ""

                for metadata in curation[area]:
                    text += metadata["label"]+": "+str(metadata["value"])+"\n"

                anno = {
                    "@id": annotation_url+"#"+str(count),
                    "@type": "oa:Annotation",
                    "motivation": "sc:painting",
                    "resource": {
                        "@type": "cnt:ContentAsText",
                        "chars": text,
                        "format": "text/plain"
                    },
                    "on": canvas_id+"#"+area
                }

                annotationlist["resources"].append(anno)

                count += 1

            with open(odir+"/"+id+"/"+anno_filename, 'w') as outfile:
                json.dump(annotationlist, outfile, ensure_ascii=False,
                          sort_keys=True, separators=(',', ': '))

    with open(odir+"/"+id+"/manifest.json", 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False,
                  sort_keys=True, separators=(',', ': '))

    # http://localhost:8888/dataset/docs/collections/tanaka/image/anno/d09a5554-d84d-4f0f-b6e9-102755e7c2fa/p0065-annolist.json
