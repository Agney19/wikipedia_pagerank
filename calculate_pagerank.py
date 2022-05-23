import numpy as np
from scipy.sparse import lil_matrix, dok_matrix, save_npz, load_npz
import time
from threading import Thread

rank_filepath = 'C:/Users/achernyshev/Documents/la_project/pagerank_result.txt'
pages_filepath = 'C:/Users/achernyshev/Documents/la_project/pages.txt'
m_filepath_pattern = 'C:/Users/achernyshev/Documents/la_project/m2-%d.npz'
convergence_threshold = 0.000_000_1
top_count = 20

def has_converged(x_next, x_prev):
    return all(abs(xi) <= convergence_threshold for xi in x_next-x_prev)

mx_count = 100
page_count = sum(1 for line in open(pages_filepath, encoding="utf8"))
start_rank = 1 / page_count
x = np.full(page_count, start_rank)
coef = 0.15

mxs = []
for i in range(1, mx_count+1):
    A = load_npz(m_filepath_pattern % (i))
    mxs.append(A)
    print('Matrix %d (%s) loaded' % (i, str(A.shape)))
start = time.time()
    
for i in range(100):
    print(i, end=' ')
    xis = [(1-coef)*mx.dot(x) + coef/page_count for mx in mxs]
    x_next = np.concatenate((xis))
    x_next = x_next / np.linalg.norm(x_next, ord=1)
    if has_converged(x_next, x):
        break
    x = x_next
    
mxs = []
print('\nPage Rank vector converged with tolerance: %s' % convergence_threshold)

pages = [line.split()[1] for line in open(pages_filepath, encoding="utf8")]
top_els = list(zip(x, pages))
top_els.sort(key=lambda el: el[0], reverse=True)
with open(rank_filepath, "w+", encoding="utf8") as f:
    f.writelines(['%s\n' % str(el) for el in top_els])
print('Execution completed in: %d sec' % (time.time() - start))