import pickle
import json

alphabet = []
idx_of_idx = {}
last_char = '-1'
for x in range(48, 97 + 26):
    if 57 >= x or x >= 97:
        char = chr(x)
        alphabet.append(char)
        with open(f'index_files/{char}_file.pkl', 'rb') as pkl_file:
            with open('inverted_index.txt', 'ab') as inv_idx_file:
                # run time update
                if last_char != char:
                    print(char)
                    last_char = char
                memory_inv_idx = pickle.load(pkl_file)
                for token in memory_inv_idx:
                    idx_of_idx[token] = inv_idx_file.tell()  # file position
                    pickle.dump(memory_inv_idx[token], inv_idx_file)

with open('idx_of_idx_var.txt', 'w') as file:
    file.write(json.dumps(idx_of_idx))