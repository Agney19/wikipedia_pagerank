import numpy as np
from scipy.sparse import lil_matrix, dok_matrix, save_npz, load_npz
import time
import threading
from threading import Thread
import pickle

pages_filepath = 'C:/Users/achernyshev/Documents/la_project/pages.txt' # they are sorted by id
links_filepath = 'C:/Users/achernyshev/Documents/la_project/pagelinks-sorted.txt'
page_link_counts_dictionary_filepath = 'C:/Users/achernyshev/Documents/la_project/page_link_counts_dictionary.pkl'
m_filepath_pattern = 'C:/Users/achernyshev/Documents/la_project/m2-%d.npz'
thread_count = 4
fraction = 100
 
pages = dict((line.split()[0], idx) for idx, line in enumerate(open(pages_filepath, encoding="utf8")))
page_total = len(pages)
link_line_total = sum(1 for line in open(links_filepath, encoding="utf8"))

print('Total page count     : %d' % (page_total))
print('Total link line count: %d' % (link_line_total))
with open(page_link_counts_dictionary_filepath, 'rb') as f:
    page_link_counts = pickle.load(f)
    
def fill_part(start_line_idx, end_line_idx, line_offset, idx_offset, rows, A):
    print('%s started: %d - %d (link line offset: %d, mx row offset %d)' % (threading.current_thread().name, start_line_idx, end_line_idx, line_offset, idx_offset))
    
    for idx in range(start_line_idx-line_offset, end_line_idx-line_offset+1):
        lar = rows[idx][:-1].split()
        to_row_idx = pages[lar[0][:-1]]
        for from_num in lar[1:]:
            A[to_row_idx-idx_offset, pages[from_num]] = 1 / page_link_counts[from_num] 
            
        if (idx-(start_line_idx-line_offset)+1) % 100 == 0:
            print('%20s: %3d %%' % ('%d - %d' % (start_line_idx, end_line_idx), 100*(idx-(start_line_idx-line_offset)+1)/(end_line_idx-start_line_idx+1)))
    print('%s finished: %d - %d (link line offset: %d, mx row offset %d)' % (threading.current_thread().name, start_line_idx, end_line_idx, line_offset, idx_offset))

def prepare_threads(start_line_idx, end_line_idx, idx_offset, A):
    rows = list(map(lambda el: el[1], filter(lambda el: start_line_idx<=el[0]<=end_line_idx, enumerate(open(links_filepath, encoding="utf8")))))
    threads = []
    line_offset = start_line_idx
    batch_size = int((end_line_idx - start_line_idx + 1) / thread_count)
    batch_end_idx = start_line_idx + batch_size
    for i in range(thread_count - 1):
        threads.append(Thread(target=fill_part, args=(start_line_idx, batch_end_idx, line_offset, idx_offset, rows, A)))
        start_line_idx = batch_end_idx + 1
        batch_end_idx = start_line_idx + batch_size - 1
    threads.append(Thread(target=fill_part, args=(start_line_idx, end_line_idx, line_offset, idx_offset, rows, A)))
    return threads

def prepare_m(start_line_idx, end_line_idx, prev_end_idx, is_last):
    if not is_last:
        end_idx = pages[list(filter(lambda el: el[0] == end_line_idx, enumerate(open(links_filepath, encoding="utf8"))))[0][1].split(': ',1)[0]]
    else:
        end_idx = page_total-1
    start_idx = prev_end_idx + 1
    A = dok_matrix((end_idx - start_idx + 1, page_total))
    print('Matrix %s initialized' % (str(A.get_shape())))
    threads = prepare_threads(start_line_idx, end_line_idx, start_idx, A)
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
    return (A, end_idx)
    
def save_m(num, A):
    filepath = m_filepath_pattern % (num)
    save_npz(filepath, A.tocsr())
    print("Saved: %s" % (filepath))

def save_m_parts():
    batch_size = int(link_line_total/fraction)
    mx_num = 1
    start_line_idx = 0
    prev_end_line_idx = -1
    while start_line_idx < link_line_total:
        end_line_idx = start_line_idx + batch_size
        if end_line_idx > link_line_total - 1:
            end_line_idx = link_line_total - 1
        print('Processing of matrix part %d started' % (mx_num))
        res = prepare_m(start_line_idx, end_line_idx, prev_end_line_idx, mx_num == fraction)
        save_m(mx_num, res[0])
        prev_end_line_idx = res[1] 
        start_line_idx = end_line_idx + 1
        mx_num += 1
    
start = time.time()
save_m_parts()
print('Execution completed in %d sec' % (time.time() - start)) 