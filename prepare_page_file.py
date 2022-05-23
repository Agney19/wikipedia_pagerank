import time

src_filepath = 'C:/Users/achernyshev/Documents/la_project/enwiki-latest-page.sql'
target_filepath = 'C:/Users/achernyshev/Documents/la_project/pages.txt'
sorted_filepath = 'C:/Users/achernyshev/Documents/la_project/pages-sorted.txt'
insert_line_start = 'INSERT INTO `page` VALUES '

total = 0
print('Pages processing started')
start = time.time()
with open(src_filepath, encoding="utf8") as src_file, open(target_filepath, "w+", encoding="utf8") as target_file:
    for line_idx, line in enumerate(src_file):
        if not line.startswith(insert_line_start):
            continue

        rows = line.split(insert_line_start)[1][1:-1].split('),(')
        for row_idx, row in enumerate(rows):
            fields = row.split(',')
            if fields[1] != '0' or fields[-9] == '1': # omit if page is redirect or not from ns0
                continue
            name = ",".join(fields[:-10][2:])[1:-1]
            target_file.write('%s %s\n' % (fields[0], name))
            total = total + 1
                
        if (line_idx + 1) % 25 == 0:
            print('%5d lines processed; Total rows taken: %d' % (line_idx + 1, total))
        
print('%5d lines processed; Total rows taken: %d' % (line_idx + 1, total))                   
print('Execution completed in %d' % (time.time() - start))   print('Sorting started')
start = time.time()
with open(src_filepath, encoding="utf8") as src_file, open(sorted_filepath, "w+", encoding="utf8") as target_file:
    lines = src_file.readlines()[:-1]
    lines.sort(key=lambda el: el.split()[1])
    target_file.writelines(lines)
print('Execution completed in %d sec' % (time.time() - start)) 
