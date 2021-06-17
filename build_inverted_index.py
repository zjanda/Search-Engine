"""
This program builds the full inverted index, and store it in inverted_index.pkl
    doc_id_dict = {doc_id : url}
    doc_id = 0 ~ total file num

    inverted_index = { token : {doc_id : Posting} }
"""

import os
import string
import json
import pickle
import math

import bs4
import nltk
from bs4 import BeautifulSoup
from nltk import WordNetLemmatizer
from urllib.parse import urldefrag

from create_doc_id import build_doc_id_dict
from posting import Posting
from time import time
from file_operations import *

clear_indexed_files()  # clear any old index files
lemmatizer = WordNetLemmatizer()  # for stemming, need to download nltk.wordnet()


def lemmatize_tokens(tokens):
    clean_tokens = []
    for t in tokens:
        clean_tokens.append(lemmatizer.lemmatize(t))
    return clean_tokens


doc_id_dict = build_doc_id_dict()
# doc_id_dict = pickle.load(open('doc_id.pkl', "rb"))
total_document_count = len(doc_id_dict)  # the N in calculating IDF

inverted_index = dict()
directory = './DEV'  # Directory of files being indexed

# Start timer
DUMP_INTERVAL = 300  # number of seconds between each save
start = round(time())
elapsed_time = int(time() - start)
last_offload_time = 0
first_run = True

for root, subdirs, files in os.walk(directory):
    for file in files:
        if file.startswith('.'):  # skip .DS_STORE
            continue

        url = json.load(open(os.path.join(root, file)))["url"]
        if url.endswith('.txt'):  # skip txt file
            continue
        fragment = urldefrag(url)[1]  # defragment, skip duplicate files
        if fragment:
            continue

        print(f"File:{doc_id_dict[url]}, URL: {url}")

        # BOLD TEXT, H1, H2, H3, TITLE, other tags, and their weight
        # source: https://www.w3schools.com/tags/ref_byfunc.asp
        html_tags = {'b': 5, 'h1': 8, 'h2': 7, 'h3': 6, 'title': 10,
                     'h4': 5, 'h5': 4, 'h6': 3, 'p': 1, 'div': 1, 'label': 2, 'meta': 4, 'span': 1, 'option': 2,
                     'legend': 2, 'blockquote': 2, 'em': 3, 'cite': 2, 'strong': 4, 'li': 2, 'td': 2, 'caption': 2,
                     'dt': 2, 'dd': 2, 'dialog': 1, 'summary': 2, 'figcaption': 4, 'del': 1, 'ins': 2, 'mark': 4,
                     'pre': 1, 'q': 2, 's': 1, 'small': 1, 'u': 1, 'var': 1}

        data = json.load(open(os.path.join(root, file)))["content"]
        soup = BeautifulSoup(data, 'html.parser')

        for tag, weight in html_tags.items():
            all_tags = soup.find_all(tag)
            if not all_tags:
                continue

            for t in all_tags:  # source: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#navigablestring
                text = ' '.join([content for content in t.contents if type(content) == bs4.element.NavigableString])
                text_tokens = nltk.regexp_tokenize(text.lower(), r"[a-zA-Z0-9]{3,25}")
                lemmatized_tokens = lemmatize_tokens(text_tokens)

                for token in lemmatized_tokens:
                    if token not in string.punctuation:  # ignore punctuations
                        doc_id = doc_id_dict[url]
                        if token in inverted_index:
                            if doc_id not in inverted_index[token]:
                                inverted_index[token][doc_id] = Posting(doc_id, weight)
                            else:
                                inverted_index[token][doc_id].update_tf(weight)
                        else:
                            inverted_index[token] = {doc_id: Posting(doc_id, weight)}

                # Run Timer and Dump to files
                if elapsed_time != int(time() - start):
                    if elapsed_time % DUMP_INTERVAL == 0 and elapsed_time != last_offload_time:
                        # offload partial index at least 3 times
                        last_offload_time = elapsed_time

                        # Save to file
                        if first_run:
                            create_index_files(inverted_index)
                            first_run = False
                        else:
                            dump_to_file(inverted_index)

                        inverted_index = {}

                    elapsed_time = int(time() - start)

# Do a final Save to file to flush everything in
if first_run:
    create_index_files(inverted_index)
    first_run = False
else:
    dump_to_file(inverted_index)

# # calculate TF-IDF
# for token, value in inverted_index.items():
#     document_freq = math.log10(total_document_count / len(value))
#     for (doc_id, posting) in value.items():
#         posting.set_tfidf(document_freq)

print(f"Number of documents: {len(doc_id_dict)}")
print(f"Number of unique tokens: {len(inverted_index)}")

# with open('inverted_index.pkl', 'wb') as file:
#     pickle.dump(inverted_index, file, protocol=4)
