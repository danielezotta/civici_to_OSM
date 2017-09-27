## Importing Housenumbers into OSM from municipality's dataset

Here you can see how I did to get the housenumbers from the municipality of Trento into OpenStreetMap, verifing which are already in OpenStreetMap and deleting from the dataset.

#### Here are all the steps I made

+ I got the dataset from both [OpenStreetMap](https://www.openstreetmap.org/){:target="_blank"} and [DatiTrentino](http://dati.trentino.it/){:target="_blank"}
+ I created a SQLite database and inserted the datasets creating 2 tables with [Spatialite-gui](https://www.gaia-gis.it/fossil/spatialite_gui/index){:target="_blank"}
+ I created a third table, based on the Municipality one, containing only "front entrance" numbers and discarding side entrances
+ I started to write some code in Python to do some exercises without Spatialite-gui
+ Then I began to write the code to get common housenumbers from the two tables and you can see the code into this file ([get_common_numbers](https://github.com/danielezotta/civici_to_OSM/blob/master/get_common_numbers.py)){:target="_blank"}
+ I installed [OpenRefine](http://openrefine.org/){:target="_blank"}, to manage and remove housenumbers with different street names, from the output of ([get_common_numbers](https://github.com/danielezotta/civici_to_OSM/blob/master/get_common_numbers.py)){:target="_blank"}
+ Once refined the output file, I wrote 
