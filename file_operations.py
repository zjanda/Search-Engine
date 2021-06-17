import pickle
import os

# first_inv_idx = {
#     'apple': {'doc_id': 'Posting'},
#     'banana': {'doc_id': 'Posting'},
#     'cat': {'doc_id': 'Posting'},
#     'ape': {'doc_id': 'Posting'}
# }
#
# memory_inv_idx1 = {
#     'apple': {'doc_id0': 'Posting', 'doc_id2': 'Posting', 'doc_id3': 'Posting', 'doc_id4': 'Posting',
#               'doc_id5': 'Posting'},
#     'for': {'doc_id1': 'Posting', 'doc_id2': 7},
#     'cat': {'doc_id2': 'Posting'},
#     "brand": {'doc_id': "Ford"},
#     "model": {'doc_id': "Mustang"},
#     "year": {'doc_id': 1964},
#     'gfg': {'doc_id': 4},
#     'is': {'doc_id': 12},
#     'best': {'doc_id': 6},
#     'geeks': {'doc_id': 10}
# }


def clear_indexed_files():
    for file in os.listdir('index_files'):
        os.remove(f'index_files/{file}')


def create_index_files(memory_inv_idx):
    alphanum_dict_dict = {}
    alphanum_list = []

    # create alpha numeric list 0-9 a-z
    for x in range(48, 97 + 26):
        if x >= 97 or 48 <= x <= 57:
            char = f'{chr(x)}'
            alphanum_list.append(char)
            alphanum_dict_dict[char] = {}   # double dictionary (value of each key is a dictionary)

    for token, docPost_dict in memory_inv_idx.items():
        alphanum_dict_dict[token[0]][token] = docPost_dict

    # Create indexed content files
    alphabet_size = len(alphanum_list)
    for char_index in range(alphabet_size):
        char = alphanum_list[char_index]
        with open(f'index_files/{char.upper()}_file.pkl', 'wb') as file:
            print(type(alphanum_dict_dict[char]))
            pickle.dump(alphanum_dict_dict[char], file)


def merge_dicts(file_inv_idx, memory_inv_idx):
    parent_inv_idx = file_inv_idx.copy()
    for token, docPost_dict in memory_inv_idx.items():
        setdefault = file_inv_idx.setdefault(token, {})
        parent_inv_idx[token] = setdefault | docPost_dict

    return dict(sorted(parent_inv_idx.items(), key=lambda x: x[0]))


def dump_to_file(memory_inv_idx):
    alphanum_dict_dict1 = {}
    alphanum_dict_dict2 = {}
    alphanum_list = []

    for x in range(48, 97 + 26):
        if x >= 97 or 48 <= x <= 57:
            char = f'{chr(x)}'
            alphanum_list.append(char)
            alphanum_dict_dict1[char] = {}
            alphanum_dict_dict2[char] = {}

    for token, docPost_dict in memory_inv_idx.items():
        first_letter = token[0]
        alphanum_dict_dict2[first_letter][token] = docPost_dict

    alphanum_size = len(alphanum_dict_dict1)
    for char_index in range(alphanum_size):
        char = alphanum_list[char_index]
        with open(f'index_files/{char.upper()}_file.pkl', 'rb') as file:
            alphanum_dict_dict1[char] = pickle.loads(file.read())

        with open(f'index_files/{char.upper()}_file.pkl', 'wb') as file:
            pickle.dump(merge_dicts(alphanum_dict_dict1[char], alphanum_dict_dict2[char]), file)