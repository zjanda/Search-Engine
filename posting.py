# define the class for posting object
import math

class Posting:
    def __init__(self, doc_id, score):
        self.doc_id = doc_id
        self.tf = score

    def update_tf(self, score):
        self.tf += score

    def get_doc_id(self):
        return self.doc_id

    def get_tf(self):
        return self.tf

    def __lt__(self, other):
        return self.tf < other.get_tf()

    def set_tfidf(self, document_freq):
        self.tf = (1 + math.log10(self.tf)) * document_freq