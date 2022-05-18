# wikipedia_pagerank

**PageRank calculation for Wikipedia articles**

**prepare_data.py** - convert preprocessed Wikipedia dump files (taken from https://dumps.wikimedia.org/enwiki/20220501/ and http://users.on.net/~henry/pagerank/) to CSR sparse matrix files (.npz). Run this before any computation
As dump data is too large to be loaded in RAM entirely. It is divided between 3 .NPZ files

**calculate.py** - calculate PageRank for obtained matrices and output top 10 articles
