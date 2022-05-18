import numpy as np
from scipy.sparse import lil_matrix, dok_matrix, save_npz, load_npz
import time
from threading import Thread

titles_filepath = 'C:/Users/achernyshev/Documents/la_project/titles-sorted.txt'
m1_filepath = 'C:/Users/achernyshev/Documents/la_project/m1.npz'
m2_filepath = 'C:/Users/achernyshev/Documents/la_project/m2.npz'
m3_filepath = 'C:/Users/achernyshev/Documents/la_project/m3.npz'
 
page_num = sum(1 for line in open(titles_filepath, encoding="utf8"))
start_rank = 1 / page_num
x = np.full(page_num, start_rank)
coef = 0.15

A1 = load_npz(m1_filepath)
print('Matrix A1 %s loaded' % str(A1.shape))
A2 = load_npz(m2_filepath)
print('Matrix A2 %s loaded' % str(A2.shape))
A3 = load_npz(m3_filepath)
print('Matrix A3 %s loaded' % str(A3.shape))
start = time.time()
    
for i in range(10):
    print('i: %d' % i)
    x1 = (1 - coef) * A1.dot(x) + coef / page_num
    x2 = (1 - coef) * A2.dot(x) + coef / page_num
    x3 = (1 - coef) * A3.dot(x) + coef / page_num
    x = np.concatenate((x1, x2, x3))
    x = x / np.linalg.norm(x, ord=1)
    
top_idxs = np.argpartition(x, -10)[-10:]
top_els = list(zip(top_idxs, x[top_idxs]))
top_els.sort(key=lambda el: el[1], reverse=True)
res = []
for el in top_els:
    with open(titles_filepath, encoding="utf8") as titles_file:
        for idx, title in enumerate(titles_file):
            if idx == el[0]:
                res.append(el + (title[:-1],))
print(' \n'.join(str(el) for el in res))
print('Execution completed in: %d sec' % (time.time() - start))