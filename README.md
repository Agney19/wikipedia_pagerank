# wikipedia_pagerank

**PageRank & HITS rank calculation for Wikipedia articles (+ keyword-inclusion search)**

Wikipedia publish dump files which should be downloaded: https://dumps.wikimedia.org/enwiki/20220501/: enwiki-latest-page.sql and enwiki-latest-pagelinks.sql \
You need at least 10 Gb of RAM to successfully finish script execution \
To parse Wikipedia dump files and calculate ranks the following scripts should be run sequentially in the specified order:

---
**prepare_page_file.py**      - parse enwiki-latest-page.sql (pages info) and store result in file in format "('id' 'article name')"

**prepare_pagelinks_file.py** - parse enwiki-latest-pagelinks.sql (page links info) and store result in file in format "'to_page_id': 'from_page_id_1' 'from_page_id_2' ..."


**sort_pages.py**             - sort file generated from prepare_page_file.py by article name and generate new file in the same format

**sort_pagelinks_file.py**    - sort file generated from prepare_pagelinks_file.py by 'to_page_id' and generate new file in the same format


**prepare_data.py**           - use previously generated files to create final all-pages-and-links-matrix divided in 100 chunks stored in .npz files (compressed scypi sparse matrices)


**calculate_pagerank.py**     - calculate PageRank for obtained matrices and store result in file in format: "('rank' 'article name')"

**pagerank_search.py**        - execute search on file generated from calculate_pagerank.py and show the most high-ranked articles

**hits.py**                   - execute search, calculate HITS ranks and show the most high-ranked articles
---

**Example: PageRank top 10 articles**
```
(0.002324391189878478,  'Geographic_coordinate_system')
(0.0011819588179895083, 'Wayback_Machine')
(0.0009234569884966509, 'United_States')
(0.0007547843356603451, 'Wikidata')
(0.0007029730511472401, 'IMDb')
(0.0006500005552535752, 'Time_zone')
(0.0006163663315405736, 'Taxonomy_(biology)')
(0.0005193907526380554, 'Global_Biodiversity_Information_Facility')
(0.0004761746414185166, 'Association_football')
(0.0004742562953533614, 'United_Kingdom')
```
