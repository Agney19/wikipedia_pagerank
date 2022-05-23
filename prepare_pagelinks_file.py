import time
import pickle

pages_filepath = 'C:/Users/achernyshev/Documents/la_project/pages-sorted.txt'
src_filepath = 'C:/Users/achernyshev/Documents/la_project/enwiki-latest-pagelinks.sql'
target_filepath = 'C:/Users/achernyshev/Documents/la_project/pagelinks.txt'
page_link_counts_dictionary_filepath = 'C:/Users/achernyshev/Documents/la_project/page_link_counts_dictionary.pkl'
insert_line_start = 'INSERT INTO `pagelinks` VALUES '

pages = dict((line.split()[1],line.split()[0]) for line in open(pages_filepath, encoding="utf8"))
page_link_counts = dict((id, 0) for id in pages.values())
print('Pagelinks processing started')
start = time.time()
not_found_links = 0
cur_to_id = None
cur_from_ids = []
total = 0
with open(src_filepath, encoding="utf8") as src_file, open(target_filepath, "w+", encoding="utf8") as target_file:
    for line_idx, line in enumerate(src_file):
        if not line.startswith(insert_line_start):
            continue

        rows = line.split(insert_line_start)[1][1:-1].split('),(')
        for row in rows:
            fields = row.split(',')
            if fields[1] != '0' or fields[-1] != '0': # omit if pagelink is not ns0 -> ns0
                continue
            from_id = fields[0]
            to_name = ','.join(fields[2:-1])[1:-1]
                
            to_id = pages.get(to_name)
            from_page_link_count = page_link_counts.get(from_id)
            if to_id == None or from_page_link_count == None: # второе условие можно убрать, если редиректы тоже будут
                not_found_links += 1
                continue
                
            if to_id == cur_to_id:
                cur_from_ids.append(from_id)
                page_link_counts[from_id] += 1
            else:
                if len(cur_from_ids) > 0:
                    target_file.write('%s: %s\n' % (cur_to_id, ' '.join(cur_from_ids)))
                    total = total + len(cur_from_ids)
                cur_from_ids = [from_id]
                page_link_counts[from_id] += 1
                cur_to_id = to_id
                       
        if (line_idx + 1) % 25 == 0:
            print('%5d lines processed; Total rows taken: %d' % (line_idx + 1, total))
     
    target_file.write('%s: %s\n' % (cur_to_id, ' '.join(cur_from_ids)))
    total = total + len(cur_from_ids)  
print('%5d lines processed; Total rows taken: %d' % (line_idx + 1, total))
    
with open(page_link_counts_dictionary_filepath, 'wb') as f:
    pickle.dump(page_link_counts, f)    
print(page_link_counts['586'])
print('Not found link count: %d' % not_found_links)    
print('Execution completed in %d sec' % (time.time() - start)) 
