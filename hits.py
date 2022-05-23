import numpy as np

p_filepath = 'C:/Users/achernyshev/Documents/la_project/pages.txt'
l_filepath = 'C:/Users/achernyshev/Documents/la_project/pagelinks-sorted.txt'
search_limit = 1000
link_limit = 100
convergence_threshold = 0.000_001
top_count = 20
keyword = 'red_square'.lower()
pages = dict((line.split()[0], line.split()[1]) for idx, line in enumerate(open(p_filepath, encoding="utf8")))

def has_converged(x_next, x_prev):
    return all(abs(xi) <= convergence_threshold for xi in x_next-x_prev)
    
search_results = []
with open(p_filepath, encoding="utf8") as f:
    for i, line in enumerate(f):
        if keyword in line.lower():
            print('%d: %s' % (i, line[:-1]))
            search_results.append(line.split()[0])
            if len(search_results) == search_limit:
                break
print('Found %d articles' % (len(search_results)))
if len(search_results) == 0:
    exit(0)
res_dict = dict((id, [[],[]]) for id in search_results) #{1: [in[2,3,4],out[5,6,7]], ...}

with open(l_filepath, encoding="utf8") as f:
    for idx, line in enumerate(f):
        if idx % 100_000 == 0:
            print(idx)
        fields = line[:-1].split(' ')
        to_id = fields[0][:-1]
        from_ids = fields[1:]
        if to_id in search_results:
            el = res_dict[to_id]
            i = 0
            while len(el[0]) < link_limit and i < len(from_ids):
                el[0].append(from_ids[i])
                i += 1
        for from_id in from_ids:
            if from_id in search_results:
                el = res_dict[from_id]
                if len(el[1]) < link_limit:
                    el[1].append(to_id)

all_ids = set(res_dict.keys())
[all_ids.update(v[0] + v[1]) for v in res_dict.values()]
id_dict     = dict((id, idx) for idx,id in enumerate(all_ids))
id_rev_dict = dict((idx, id) for id,idx in id_dict.items())
page_num = len(all_ids)
print('Page num: %d' % (page_num))
L = np.zeros((page_num, page_num))

for id,link_ids in res_dict.items():
    idx = id_dict[id]
    for in_link_page_id in link_ids[0]:
        L[id_dict[in_link_page_id], idx] = 1
    for out_link_page_id in link_ids[1]:
        L[idx, id_dict[out_link_page_id]] = 1
        
Lt = L.transpose()
y = np.ones((page_num,))

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
hub_ranks = [(pages[id_rev_dict[idx]], rank) for idx,rank in enumerate(y)]
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
auth_ranks = [(pages[id_rev_dict[idx]], rank) for idx,rank in enumerate(x)]
auth_ranks.sort(key=lambda el: el[1], reverse=True)
print('Top %d Authorities:\n%s' % (top_count, '\n'.join([str(el) for el in auth_ranks[:top_count]])))


