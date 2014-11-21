WIGI
====

Wikipedia Gender Index (WIGI), uses Wikidata to produce gender-related statistic on Wikipedia Biographies

+ __The__ [__paper__ so far on google docs](https://docs.google.com/document/d/1RbXH0hBp5Y_HqXUcpSUZ4d3c5Y_AhNKEmIhGdV9FF4U/edit?usp=sharing) please comment.
+ In progress [__discussion__](https://meta.wikimedia.org/wiki/Research_talk:Wikipedia_Gender_Inequality_Index) on meta.
+ The __raw [data file](https://github.com/notconfusing/WIGI/blob/master/snapshot_data/2014-10-13/gender-index-data-2014-10-13.csv.gz)__ (csv) one row per human in Wikidata, including their place of, and date of birth, death, ethnicity, and citizenship (if they exist).
+ [__Re-indexed data__](https://github.com/notconfusing/WIGI/tree/master/snapshot_data/2014-10-13/property_indexes) files, one per each property, by sex (e.g. [date of birth by sex](https://github.com/notconfusing/WIGI/blob/master/snapshot_data/2014-10-13/property_indexes/dob-index.csv))
+ And some helper [files to __aggregate and map__](https://github.com/notconfusing/WIGI/tree/master/helpers/aggregation_maps) place of birth, ethnicity, and citizenship into "world cultures".
+ Plus, some Ipython notebooks on how to:
  + munge and plot the [intitial file and make the reindexes](http://nbviewer.ipython.org/github/notconfusing/WIGI/blob/master/gender-index-processing.ipynb)
  + look at [world cultures by date of birth and gender over time](http://nbviewer.ipython.org/github/notconfusing/WIGI/blob/master/World%20Cultures%20Analysis.ipynb)
