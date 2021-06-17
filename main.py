"""
This main program that prompts the user for a query, do search, and return results
"""


import pickle
import json
import nltk
import math
from nltk.corpus import stopwords
from nltk import WordNetLemmatizer
from posting import Posting
from time import time

doc_id_for_printing = pickle.load(open('doc_id_for_printing.pkl', "rb"))
total_document_count = len(doc_id_for_printing)  # the N in calculating IDF


def filter_query(query, lemmatizer):
    stop_words = set(stopwords.words('english'))
    query_tokens = nltk.regexp_tokenize(query.strip().lower(), r"[a-zA-Z0-9]{1,}")

    result = []
    for t in query_tokens:
        if t not in stop_words:
            result.append(lemmatizer.lemmatize(t))
    return result


#  Return a list of {doc_id, posting} for each token
def get_posting_list(query_tokens, idx_of_idx, inv_idx_file):
    posting_list = []
    for token in query_tokens:
        if token not in idx_of_idx:  # ignore words that are not present in inverted index
            continue
        inv_idx_file.seek(idx_of_idx[token])
        posting = pickle.load(inv_idx_file)
        # calculate TF-IDF
        document_freq = math.log10(total_document_count / len(posting))
        for (doc_id, p) in posting.items():
            p.set_tfidf(document_freq)
        posting_list.append(posting)
    return posting_list


def print_url(posting_list):
    posting_list.sort(key= lambda i : i.get_tf(), reverse=True)  # rank based on tf-idf score
    print('This search took', time() - start, 'seconds.')

    limit = 10   # ** how many results to show
    limit = min(limit, len(posting_list))
    for posting in posting_list:
        if (limit > 0):
            doc_id = posting.get_doc_id()
            print(f"({posting.get_tf():.3f}) {doc_id}: {doc_id_for_printing[doc_id]}")
            limit -= 1


def main():
    with open('idx_of_idx_var.txt', 'r') as file:
        idx_of_idx = json.loads(file.read())
    with open('inverted_index.txt', 'rb') as inv_idx_file:
        lemmatizer = WordNetLemmatizer()
        lemmatizer.lemmatize('')  # prime the lemmatizer for use

        print("Welcome to ICS Search!")
        while True:
            query = input("Search: ")
            global start
            start = time()
            query_tokens = filter_query(query, lemmatizer)
            posting_list = get_posting_list(query_tokens, idx_of_idx, inv_idx_file)  # a list of {doc_id, posting}

            if (len(posting_list)) == 0:
                print('There is no result found. Try a different query.')
                continue

            # conjunctive processing (skip doc id that do not contain all query terms)
            posting_a = posting_list[0]  # initialize as 1st {doc_id, posting}
            intersect_doc_id = posting_a.keys()
            for i in range(1, len(posting_list)):
                posting_b = posting_list[i]
                intersect_doc_id &= posting_b.keys()

            intersection_posting_list = []  # [Posting(doc_id, total_score)]
            for k in intersect_doc_id:
                total_score = 0  # each doc_id has a total score (add each posting tf together)
                for d in posting_list:
                    total_score += d[k].get_tf()
                intersection_posting_list.append(Posting(k, total_score))

            print(f"total results: {len(intersection_posting_list)}")
            print_url(intersection_posting_list)


if __name__ == "__main__":
    main()
