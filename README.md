WIGI
====

Wikipedia Gender Index (WIGI), uses Wikidata to produce gender-related statistic on Wikipedia Biographies

##The Data
+ The __raw [data file](https://github.com/notconfusing/WIGI/blob/master/snapshot_data/2014-10-13/gender-index-data-2014-10-13.csv.gz)__ (csv) one row per human in Wikidata, including their place of, and date of birth, death, ethnicity, and citizenship (if they exist).
+ [__Re-indexed data__](https://github.com/notconfusing/WIGI/tree/master/snapshot_data/2014-10-13/property_indexes) files, one per each property, by sex (e.g. [date of birth by sex](https://github.com/notconfusing/WIGI/blob/master/snapshot_data/2014-10-13/property_indexes/dob-index.csv))
+ And some helper [files to __aggregate and map__](https://github.com/notconfusing/WIGI/tree/master/helpers/aggregation_maps) place of birth, ethnicity, and citizenship into "world cultures".


## Data Munging Documentation Ipython Notebooks
+ Plus, some Ipython notebooks on how to:
  + munge and plot the [intitial file and make the reindexes](http://nbviewer.ipython.org/github/notconfusing/WIGI/blob/master/gender-index-processing.ipynb)
  + look at [world cultures by date of birth and gender over time and how to aggregate the cultures](http://nbviewer.ipython.org/github/notconfusing/WIGI/blob/master/World%20Cultures%20Analysis.ipynb)
   + [Chi Squared Testing of Gender versus Culture](http://nbviewer.ipython.org/github/notconfusing/WIGI/blob/master/Chi%20squared%20test.ipynb) and [pretty plots of the same](http://nbviewer.ipython.org/github/notconfusing/WIGI/blob/master/Gender%20Culture%20Plots.ipynb)
   + How to make data for and test the [celebrity hypothesis](http://nbviewer.ipython.org/github/notconfusing/WIGI/blob/master/Country%20Inspector%20Analysis%20Generator.ipynb)
   + Investigation into the [Germanic Nationality Classification Shift](http://nbviewer.ipython.org/github/notconfusing/WIGI/blob/master/German%20Austrian%20Analysis.ipynb)
   + Aggregating sitelinks into a [language-culture female percentage scatter plot](http://nbviewer.ipython.org/github/notconfusing/WIGI/blob/master/Language%20Culture%20Scatter.ipynb)
   + Modelling [female percentage of biographies for prediction](http://nbviewer.ipython.org/github/notconfusing/WIGI/blob/master/Logistics%20Fem%20Per.ipynb)
   + Scraping out the [mechanical turk disagreements for hand coding](http://nbviewer.ipython.org/github/notconfusing/WIGI/blob/master/Mechanical%20Turk%20Disagreements.ipynb)
   + How to make the [sitelinks scatter plots](http://nbviewer.ipython.org/github/notconfusing/WIGI/blob/master/Sitelinks%20Exmaple.ipynb)
   + [Comparing WIGI to the world economic forum](http://nbviewer.ipython.org/github/notconfusing/WIGI/blob/master/World%20Economic%20Forum%20Comparison.ipynb)

##The Writings
+ __The__ [__paper__ so far on google docs](https://docs.google.com/document/d/1RbXH0hBp5Y_HqXUcpSUZ4d3c5Y_AhNKEmIhGdV9FF4U/edit?usp=sharing) please comment.
+ In progress [__discussion__](https://meta.wikimedia.org/wiki/Research_talk:Wikipedia_Gender_Inequality_Index) on meta.
