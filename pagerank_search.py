import numpy as np

rank_filepath = 'C:/Users/achernyshev/Documents/la_project/pagerank_result.txt'
top_count = 20
keyword = 'yandex'.lower()

def has_converged(x_next, x_prev):
    return all(abs(xi) <= convergence_threshold for xi in x_next-x_prev)
    
search_results = []
with open(rank_filepath, encoding="utf8") as f:
    for line in f:
        if keyword in line.split(',',1)[1].lower():
            search_results.append(line[:-1])
            if len(search_results) == top_count:
                break

print('Top %d Articles:\n%s' % (top_count, '\n'.join(['(%19.18f, %s' % (float(el.split(',',1)[0][1:]), el.split(',',1)[1]) for el in search_results])))
