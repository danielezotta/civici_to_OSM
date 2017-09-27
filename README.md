## Importing Housenumbers into OSM from Trento municipality's dataset with Python 2.7

Here you can see how I did to get the housenumbers from the municipality of Trento into OpenStreetMap, verifing which are already in OpenStreetMap and deleting from the dataset.

#### Here are all the steps I made

1. I got the dataset from both [OpenStreetMap](https://www.openstreetmap.org/) and [DatiTrentino](http://dati.trentino.it/)
1. I created a SQLite database and inserted the datasets creating 2 tables with [Spatialite-gui](https://www.gaia-gis.it/fossil/spatialite_gui/index)
1. I created a third table, based on the Municipality one, containing only "front entrance" numbers and discarding side entrances
1. I started to write some code in Python to do some exercises without Spatialite-gui
1. Then I began to write the code to get common housenumbers from the two tables ([get_common_numbers](../blob/master/get_common_numbers.py))
1. I installed [OpenRefine](http://openrefine.org/), to manage and remove housenumbers with different street names, from the output of [get_common_numbers](https://github.com/danielezotta/civici_to_OSM/blob/master/get_common_numbers.py)
1. Once refined the output file, I wrote the file [delete_civici_comune](../blob/master/delete_civici_comune.py) to delete all the common housenumbers from the table
1. I done another time from the 5th point, but this time with a bigger Buffer (50m) for intersecting housenumbers that were at an higher distance
1. Estracted in a CSV file (**civici_osm.csv**) all the OpenStreetMap housenumbers, then with the file [osm_only_search](../blob/master/osm_only_search.py) I've isolated in a CSV file all the numbers not contained in the municipality's table
1. I controlled by hand all the numbers in OpenStreetMap from the previous file, changed data where needed and deleted from the municipality table (to have no copies of the same housenumber)
1. Managed to get all Municipality's street a corresponding one to OpenStreetMap, importing the roads datasets from both OpenStreetMap and the municipality, done with [get_street_comuni](../blob/master/get_street_names_comuni.py) primarily, secondly with [get_street_names](../blob/master/get_street_names.py), and at the end with [get_street_names_notinosm](../blob/master/get_street_names_notinosm.py)
1. Wrote the [import_osmapi](../blob/master/import_osmapi.py) in order to import the housenumbers into OpenStreetMap using [osmapi](https://github.com/metaodi/osmapi) for Python.
