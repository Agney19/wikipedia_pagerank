# wikipedia_pagerank

**PageRank calculation for Wikipedia articles**

**prepare_data.py** - convert preprocessed Wikipedia dump files (taken from https://dumps.wikimedia.org/enwiki/20220501/ and http://users.on.net/~henry/pagerank/) to CSR sparse matrix files (.npz). Run this before any computation

As dump data is too large to be loaded in RAM entirely. It is divided between 3 .NPZ files. You need at least 10 Gb of RAM to successfully finish script execution

**calculate.py** - calculate PageRank for obtained matrices and output top 10 articles

**Results**

Page Rank  Page name
       
 0.00222    United_States
  
 0.00141    2007
  
 0.00136    2008
  
 0.00126    Geographic_coordinate_system
  
 0.00101    United_Kingdom
  
 0.00087    2006
  
 0.00074    France
  
 0.00073    Wikimedia_Commons
  
 0.00066    Wiktionary
  
 0.00065    Canada
