# Create doc_id_dict, store in doc_id.pkl
# {doc_id : url}


import os
import json
import pickle
from urllib.parse import urldefrag


def build_doc_id_dict():
    doc_id_dict = dict()
    doc_id_for_printing = dict()
    id = 0  # ** UNIQUE id for each doc

    for root, dirs, files in os.walk("./DEV"):
        for f in files:
            if not f.startswith('.'):
                url = json.load(open(os.path.join(root, f)))["url"]

                # defrag the url, then ignore duplicate pages
                url = urldefrag(url)[0]
                if url in doc_id_dict:
                    continue

                if not url.endswith('.txt'):
                    doc_id_dict[url] = id
                    doc_id_for_printing[id] = url
                    id += 1

    with open('doc_id.pkl', 'wb') as file:
        pickle.dump(doc_id_dict, file, protocol=4)
    with open('doc_id_for_printing.pkl', 'wb') as file:
        pickle.dump(doc_id_for_printing, file, protocol=4)
    # print(len(doc_id_dict))
    return doc_id_dict

build_doc_id_dict()