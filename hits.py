import numpy as np
from scipy.sparse import load_npz
import time

m_filepath_pattern = 'C:/Users/achernyshev/Documents/la_project/ru-m2-%d.npz'
p_filepath = 'C:/Users/achernyshev/Documents/la_project/ru-pages.txt'
l_filepath = 'C:/Users/achernyshev/Documents/la_project/ru-pagelinks-sorted.txt'
mx_count = 100
search_limit = 100
link_limit = 5
convergence_threshold = 0.000_001
top_count = 25
keyword = '(телесериал)'.lower()
pages = dict((idx, line.split()[1]) for idx, line in enumerate(open(p_filepath, encoding="utf8")))
page_total = len(pages)

def has_converged(x_next, x_prev):
    return all(abs(xi) <= convergence_threshold for xi in x_next-x_prev)

search_results_idxs = []
for idx, name in enumerate(pages.values()):
    if keyword in name.lower():
        print('%d: %s' % (idx, name))
        search_results_idxs.append(idx)
        if len(search_results_idxs) == search_limit:
            break
print('Found %d articles' % (len(search_results_idxs)))
if len(search_results_idxs) == 0:
    exit(0)
# load matrices
mxs = []
mx_row_counts = []
cur_num = 0
for i in range(1, mx_count+1):
    M = load_npz(m_filepath_pattern % (i))
    mxs.append(M)
    cur_num += M.shape[0]
    mx_row_counts.append(cur_num)
    print('Matrix %d (%s) loaded. Idxs: %d - %d' % (i, str(M.shape), cur_num-M.shape[0], cur_num-1))
start = time.time()

all_idxs = set(search_results_idxs)
in_link_counts = dict((idx, 0) for idx in all_idxs)
out_link_counts = dict((idx, 0) for idx in all_idxs)
offset = 0

def process_mx_for_match(mx_idx, idx, offset):
    M = mxs[mx_idx]
    for rel_i in range(M.shape[0]):
        i = rel_i + offset
        if rel_i % 10000 == 0:
            print("Mx %d: Idx: %d - %d (%d)" % (mx_idx+1, idx, i, rel_i))
        if idx == i and out_link_counts[idx] < link_limit:
            for j in range(page_total):
                if M[rel_i,j] != 0:
                    all_idxs.add(j)
                    out_link_counts[idx] += 1
                    if out_link_counts[idx] == link_limit:
                        break
        if M[rel_i,idx] != 0 and in_link_counts[idx] < link_limit:
            all_idxs.add(i)
            in_link_counts[idx] += 1

for mx_idx in range(mx_count):
    print("Mx %d" % (mx_idx+1))
    for idx in search_results_idxs:
        if in_link_counts[idx] < link_limit or out_link_counts[idx] < link_limit:
            process_mx_for_match(mx_idx, idx, offset)
    offset += mxs[mx_idx].shape[0]
    
all_idxs = list(all_idxs)
L_len = len(all_idxs)
print('Page num: %d' % (L_len))
print(all_idxs)

# prepare adjacency matrix L
def check_link(row_idx, col_idx):
    offset = 0
    for M in mxs:
        row_count = M.shape[0]
        if row_idx < row_count + offset:
            return M[row_idx - offset, col_idx] != 0
        offset = row_count

L = np.zeros((L_len, L_len))
for l_idx1, m_idx1 in enumerate(all_idxs):
    for l_idx2, m_idx2 in enumerate(all_idxs):
        if check_link(m_idx1, m_idx2):
            L[l_idx2, l_idx1] = 1

print("Started calculation")        
Lt = L.transpose()
y = np.ones((L_len,))
x = Lt.dot(y)
x = x / np.linalg.norm(x, ord=1)

for i in range(100):
    print(i, end=' ')
    y_next = L.dot(Lt).dot(y)
    y_next = y_next / np.linalg.norm(y_next, ord=1)
    if has_converged(y_next, y):
        break
    y = y_next
    
print('\nHubs vector converged with tolerance: %s' % convergence_threshold)
hub_ranks = [(pages[all_idxs[idx]], rank) for idx,rank in enumerate(y)]
hub_ranks.sort(key=lambda el: el[1], reverse=True)
print('Top %d Hubs:\n%s\n' % (top_count, '\n'.join([str(el) for el in hub_ranks[:top_count]])))

for i in range(100):
    print(i, end=' ')
    x_next = Lt.dot(L).dot(x)
    x_next = x_next / np.linalg.norm(x_next, ord=1)
    if has_converged(x_next, x):
        break
    x = x_next
    
print('\nAuthority vector converged with tolerance: %s' % convergence_threshold)
auth_ranks = [(pages[all_idxs[idx]], rank) for idx,rank in enumerate(x)]
auth_ranks.sort(key=lambda el: el[1], reverse=True)
print('Top %d Authorities:\n%s' % (top_count, '\n'.join([str(el) for el in auth_ranks[:top_count]])))


