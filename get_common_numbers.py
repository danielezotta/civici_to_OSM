#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 10:20:46 2017

@author: daniele
"""

import sqlite3
import difflib
from postal.expand import expand_address
import time
import jellyfish
import csv


def main():

    db = '../db.sqlite'
    connection = sqlite3.connect(db)
    connection.row_factory = sqlite3.Row
    connection.enable_load_extension(True)
    cursor = connection.cursor()
    cursor.execute('SELECT load_extension("mod_spatialite")')
    
    start_time = time.time()
    
    cursor.execute("""SELECT pro.pk_uid AS ID_PROV, 
                   osm.pk_uid AS ID_OSM,
                   pro.civico_alf AS numero_provincia,
                   osm.housenumbe AS numero_osm,
                   pro.desvia AS via_prov,
                   osm.street AS via_osm,
                   pro.sobborgo AS sobborgo,
                   Y(Transform(pro.Geometry, 4326)) AS LAT,
                   X(Transform(pro.Geometry, 4326)) AS LON
                   FROM civici_prov_principali AS pro,
                   civici_osm AS osm
                   WHERE osm.ROWID IN (
                    	SELECT ROWID
                    	FROM SpatialIndex
                    	WHERE f_table_name = 'civici_osm'
                    	AND search_frame = buffer(pro.Geometry, 20))
                   AND numero_osm like numero_provincia""")
    
    civici = cursor.fetchall()

    end_time = time.time()
    print "Tempo impiegato : ", end_time - start_time
    start_time = time.time()

    to_file_all(civici)
    
    end_time = time.time()
    print "Tempo impiegato : ", end_time - start_time


def to_file_all(civici):
    
    csvfile = open("file_controllo.csv", "w")
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(["ID PROVINCIA", "ID OSM", "VIA COMUNE", "VIA NORMALIZZATA COMUNE", "VIA OSM",
                         "VIA NORMALIZZATA OSM", "LAT", "LON", "INDICE difflib", "INDICE jellyfish(Jaro-Winkler)", "ULIMA PAROLA"])
    
    for civico in civici:
        
        via_prov = civico["via_prov"].lower().replace(".", "")
        via_osm = civico["via_osm"].lower().replace(".", "")
        
        s = None
        s = difflib.SequenceMatcher(None, via_prov, via_osm)
        sm_ratio = s.quick_ratio()
        
        jw_ratio = jellyfish.jaro_winkler(via_osm, via_prov)
        
        last_via_prov = via_prov.split(" ")[-1]
        last_via_osm = via_osm.split(" ")[-1]
        
        if (sm_ratio >= 0.8 or jw_ratio > 0.91):
            filewriter.writerow([civico["ID_PROV"], civico["ID_OSM"],
                             civico["via_prov"].encode('utf-8'), 
                             expand_address(civico["via_prov"], languages=["it"]),
                             civico["via_osm"].encode('utf-8'), 
                             expand_address(civico["via_osm"], languages=["it"]),
                             civico["LAT"], civico["LON"],
                             sm_ratio, jw_ratio, 1 if last_via_prov.encode('utf-8') == last_via_osm.encode('utf-8') else 0])
    
        elif (sm_ratio >= 0.6 and last_via_prov.encode('utf-8') == last_via_osm.encode('utf-8')):
            filewriter.writerow([civico["ID_PROV"], civico["ID_OSM"],
                             civico["via_prov"].encode('utf-8'), 
                             expand_address(civico["via_prov"], languages=["it"]),
                             civico["via_osm"].encode('utf-8'), 
                             expand_address(civico["via_osm"], languages=["it"]),
                             civico["LAT"], civico["LON"],
                             sm_ratio, jw_ratio, 1])
        else:
            filewriter.writerow([civico["ID_PROV"], civico["ID_OSM"],
                             civico["via_prov"].encode('utf-8'), 
                             expand_address(civico["via_prov"], languages=["it"]),
                             civico["via_osm"].encode('utf-8'), 
                             expand_address(civico["via_osm"], languages=["it"]),
                             civico["LAT"], civico["LON"],
                             sm_ratio, jw_ratio, 0])
    

def to_file_matching(civici):
    
    csvfile = open("file.csv", "w")
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(["ID PROVINCIA", "ID OSM", "VIA COMUNE", "VIA NORMALIZZATA COMUNE", "VIA OSM",
                         "VIA NORMALIZZATA OSM", "X", "Y" "INDICE difflib", "INDICE jellyfish(Jaro-Winkler)", "ULIMA PAROLA"])
    
    for civico in civici:
        
        via_prov = civico["via_prov"].lower().replace(".", "")
        via_osm = civico["via_osm"].lower().replace(".", "") #expand_address(civico["via_osm"], languages=["it"])[0]
        
        s = None
        s = difflib.SequenceMatcher(None, via_prov, via_osm)
        sm_ratio = s.quick_ratio()
        
        jw_ratio = jellyfish.jaro_winkler(via_osm, via_prov)
        
        last_via_prov = via_prov.split(" ")[-1]
        last_via_osm = via_osm.split(" ")[-1]
        
        if (sm_ratio >= 0.80 or jw_ratio > 0.91):
            filewriter.writerow([civico["ID_PROV"], civico["ID_OSM"],
                                 civico["via_prov"].encode('utf-8'), 
                                 expand_address(civico["via_prov"], languages=["it"]),
                                 sm_ratio, jw_ratio, 1 if last_via_prov.encode('utf-8') == last_via_osm.encode('utf-8') else 0])
        else:
            if (last_via_prov == last_via_osm and sm_ratio >= 0.6):
                filewriter.writerow([civico["ID_PROV"], civico["ID_OSM"],
                                 civico["via_prov"].encode('utf-8'), 
                                 expand_address(civico["via_prov"], languages=["it"]),
                                 sm_ratio, jw_ratio, 1])
            else:
                print " X ", civico["numero_provincia"], via_prov, via_osm, sm_ratio, jellyfish.jaro_winkler(via_osm, via_prov)
    

if __name__ == "__main__":
    main()
