## Importing Housenumbers into OSM from Trento municipality's dataset with Python 2.7

Here you can see how I did to get the housenumbers from the municipality of Trento into OpenStreetMap, verifing which are already in OpenStreetMap and deleting from the dataset.

#### Here are all the steps I made

1. I got the dataset with the [address numbers](http://www.comune.trento.it/Aree-tematiche/Cartografia/Download/Numeri-civici-Open-Data) of Trento from the [Open Data section of the Municipality website](http://www.comune.trento.it/Aree-tematiche/Cartografia/Download). The dataset [is distributed with the terms of the CC0](http://www.comune.trento.it/Classificazioni/Tipi-di-licenze/CC-Zero).
1. I got the dataset with the address numbers of Trento from [OpenStreetMap](https://www.openstreetmap.org/) from the website [Estratti OpenStreetMap](http://estratti.openstreetmap.it). The file used is the shapefile *addresses.shp* archived on the zipfile [022205---Trento.zip](http://osm-estratti.wmflabs.org/estratti/comuni/shape/022205---Trento.zip)
1. I created a SQLite/Spatialite database and inserted the datasets creating 2 tables with [Spatialite-gui](https://www.gaia-gis.it/fossil/spatialite_gui/index). The projection used by the Municipality is the *ETRS89 / UTM zone 32N* [EPSG:3044](https://epsg.io/3044).
1. I created a third table, based on the Municipality one, containing only "front entrance" (value "ingresso principale") numbers and discarding side entrances.
1. I started to write some code in Python to do some exercises without Spatialite-gui
1. Then I began to write the code to get common housenumbers from the two tables ([get_common_numbers](../blob/master/get_common_numbers.py)). To improve it I used the library [pypostal](https://github.com/openvenues/pypostal) to normalize the names.
1. I cleaned the data with [OpenRefine](http://openrefine.org/) in order to remove housenumbers with different street names, from the output of [get_common_numbers](https://github.com/danielezotta/civici_to_OSM/blob/master/get_common_numbers.py)
1. I checked and corrected manually the data inside OpenStreetMap
1. Once refined the output file, I wrote the file [delete_civici_comune](../blob/master/delete_civici_comune.py) to delete all the common housenumbers from the table
1. I done another time from the 8th point, but this time with a bigger Buffer (50m - expressed with the projection [EPSG:3044](https://epsg.io/3044)) for intersecting housenumbers that were at an higher distance
1. Estracted in a CSV file (**civici_osm.csv**) all the OpenStreetMap housenumbers, then with the file [osm_only_search](../blob/master/osm_only_search.py) I've isolated in a CSV file all the numbers not contained in the municipality's table
1. I controlled by hand all the numbers in OpenStreetMap from the previous file, changed data where needed and deleted from the municipality table (to have no copies of the same housenumber)
1. Managed to get all Municipality's street a corresponding one to OpenStreetMap, importing the roads datasets from both OpenStreetMap and the municipality, done with [get_street_comuni](../blob/master/get_street_names_comuni.py) primarily, secondly with [get_street_names](../blob/master/get_street_names.py), and at the end with [get_street_names_notinosm](../blob/master/get_street_names_notinosm.py)
1. Wrote the [import_osmapi](../blob/master/import_osmapi.py) in order to import the housenumbers into OpenStreetMap using [osmapi](https://github.com/metaodi/osmapi) for Python.
