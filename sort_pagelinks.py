import time

src_filepath = 'C:/Users/achernyshev/Documents/la_project/pagelinks.txt'
target_filepath = 'C:/Users/achernyshev/Documents/la_project/pagelinks-sorted.txt'

start = time.time()
with open(src_filepath, encoding="utf8") as src_file, open(target_filepath, "w+", encoding="utf8") as target_file:
    lines = src_file.readlines()
    lines.sort(key=lambda el: int(el.split(': ', 1)[0]))
    target_file.writelines(lines)
    
print('Execution completed in %d sec' % (time.time() - start)) 
