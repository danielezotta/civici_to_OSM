#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 10:53:14 2017

@author: daniele
"""


import sqlite3
import difflib
import time
import csv


def main():

    db = '../db.sqlite'
    connection = sqlite3.connect(db)
    connection.row_factory = sqlite3.Row
    connection.enable_load_extension(True)
    cursor = connection.cursor()
    cursor.execute('SELECT load_extension("mod_spatialite")')
    
    start_time = time.time()
    
    cursor.execute("""SELECT osm.name as via_osm, pro.desvia as via_pro 
                    FROM roads_osm as osm, roads_prov as pro 
                    WHERE osm.ROWID IN (SELECT ROWID
                    FROM SpatialIndex
                    WHERE f_table_name = 'roads_osm'
                    AND search_frame = buffer(pro.Geometry, 2.5))
                    AND (via_osm != "" and via_pro != "")
                    ORDER BY via_osm desc""")
    
    vie = cursor.fetchall()

    end_time = time.time()
    print "Tempo impiegato : ", end_time - start_time
    start_time = time.time()

    to_file_all(vie)
    
    end_time = time.time()
    print "Tempo impiegato : ", end_time - start_time


def to_file_all(vie):
    
    vv = list()
    
    with open("vie_comune_osm.csv") as f:
        filereader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for r in filereader:
            vv.append(r[0])
    
    print vv
    
    csvfile = open("vie_comune_osm_ver2.csv", "w")
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    for via in vie:
        
        via_prov = via["via_pro"].lower()
        via_osm = via["via_osm"].lower()
        
        last_via_prov = via_prov.split(" ")[-1]
        last_via_osm = via_osm.split(" ")[-1]
        
        s = None
        s = difflib.SequenceMatcher(None, via_prov, via_osm)
        sm_ratio = s.quick_ratio()
        
        if (via["via_pro"] not in vv):
            if (via_prov == via_osm):
                filewriter.writerow([via["via_pro"].encode('utf8'), via["via_osm"].encode('utf8')])
                vv.append(via["via_pro"])
            elif (last_via_osm == last_via_prov and sm_ratio > 0.65):
                filewriter.writerow([via["via_pro"].encode('utf8'), via["via_osm"].encode('utf8')])
                vv.append(via["via_pro"])

if __name__ == "__main__":
    main()
