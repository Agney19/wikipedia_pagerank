import numpy as np
from scipy.sparse import lil_matrix, dok_matrix, save_npz, load_npz
import time
from threading import Thread

titles_filepath = 'C:/Users/achernyshev/Documents/la_project/titles-sorted.txt'
links_filepath = 'C:/Users/achernyshev/Documents/la_project/links-simple-sorted.txt'
m1_filepath = 'C:/Users/achernyshev/Documents/la_project/m1.npz'
m2_filepath = 'C:/Users/achernyshev/Documents/la_project/m2.npz'
m3_filepath = 'C:/Users/achernyshev/Documents/la_project/m3.npz'
 
page_num = sum(1 for line in open(titles_filepath, encoding="utf8"))

def fill_part(start_num, end_num, offset, A):
    print('Started: %d - %d' % (start_num, end_num))
    with open(links_filepath, encoding="utf8") as links_file:
        for idx, line in enumerate(links_file):
            if idx % 100_000 == 0 and idx != 0:
                print('%d - %d: %d %%' % (start_num, end_num, 100*idx/page_num))
            lar = line.split(': ')
            from_num = lar[0]
            to_nums_all = lar[1].split()
            value = 1 / len(to_nums_all)
            to_nums = list(filter(lambda num: num>=start_num and num<=end_num, 
                map(lambda str_num: int(str_num), to_nums_all)))
            for num in to_nums:
                A[num - 1 - offset, int(from_num) - 1] = value 
    print('Finished: %d - %d' % (start_num, end_num))

def prepare_part(start_num, end_num):
    A = dok_matrix((end_num - start_num + 1, page_num))
    q2_end = int((end_num-start_num)/2)+start_num
    q1_end = int((q2_end-start_num)/2)+start_num
    q3_end = int((end_num-q2_end)/2) + q2_end
    t1 = Thread(target = fill_part, args = (start_num, q1_end, start_num-1, A))
    t2 = Thread(target = fill_part, args = (q1_end+1, q2_end, start_num-1, A))
    t3 = Thread(target = fill_part, args = (q2_end+1, q3_end, start_num-1, A))
    t4 = Thread(target = fill_part, args = (q3_end+1, end_num, start_num-1, A))
    t1.start(); t2.start(); t3.start(); t4.start()
    t1.join(); t2.join(); t3.join(); t4.join()
    return A
    
start = time.time()
one_third = int(page_num/3)
save_npz(m1_filepath, prepare_part(1, one_third).tocsr())
print("Saved: " + m1_filepath)
save_npz(m2_filepath, prepare_part(one_third + 1, one_third * 2).tocsr())
print("Saved: " + m2_filepath)
save_npz(m3_filepath, prepare_part(one_third * 2 + 1, page_num).tocsr())
print("Saved: " + m3_filepath)
print("Preparation finished!")