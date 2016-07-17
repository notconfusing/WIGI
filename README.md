WIGI
====

Wikipedia Gender Index (WIGI), uses Wikidata to produce gender-related statistic on Wikipedia Biographies

##The Data
+ For __non-programmer researchers__: A simple __canonical version__ of our data, which is translated into English, is available at [Figshare](https://figshare.com/articles/Wikidata_Human_Gender_Indicators/3100903). https://figshare.com/articles/Wikidata_Human_Gender_Indicators/3100903 
+ Programmers may explore the language-agnostic, longitudintal data at http://wigi.wmflabs.org/snapshot_data/ .
++ Some helper [files to __aggregate and map__](https://github.com/notconfusing/WIGI/tree/master/helpers/aggregation_maps) place of birth, ethnicity, and citizenship into "world cultures".


## Data Munging Documentation Ipython Notebooks
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

##Notes Because Wikidata is multilingual its values are stored as identifiers - or ``Q-IDs'' in Wikidata terms - which can be translated into every language for which there is a Wikipedia language edition. To maintain fidelity we keep this standard, so for example Aung San Suu Kyi represented in Wikidata in English looks like Figure \ref{fig:aung} and in our dataset would be a row like \begin{small} Q36740,1945,,Q6581072|,,Q836|,Q37995|,,Q82955|Q36180|Q1476215|
\end{small}. As a design decision we do not translate these Wikidata Q-IDs, to maintain language neutrality. We do however include functions to translate these Q-IDs into English (or any other language), which would render the above row as: \\
\begin{small} Aung San Suu Kyi,1945,,female|,,Myanmar|,Yangon|,,politician|writer|human rights activist|
\end{small} 

In order to faithfully represent Wikidata, the value of each property is actually a list, since Wikidata allows there to potentially be multiple values for a property. This is because either two sources disagree on a property, or like in the case of Aung San Suu Kyi, she has many occupations, see Figure \ref{fig:aung}. We store the list, inside the comma-separated sheet, as | ``pipe''-separated values.

Of course these multiple values introduce a design problem in aggregating on a list of properties. Our method is to aggregate on the list, rather than on the individual items within the list. This means in the case of Aung San Suu Kyi, that her occupation is stored as politician, writer, and human rights activist, and is aggregated with all the other humans who have those three occupations too. Since the dataset is open, interested researchers can use our raw data and aggregate it in any way they want.

