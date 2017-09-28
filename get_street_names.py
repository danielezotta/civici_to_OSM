#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 10:53:14 2017

@author: Daniele Zotta <danielezotta@gmail.com>

MIT License

Copyright (c) 2017 Daniele Zotta and Fondazione Bruno Kessler

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""


import sqlite3
import difflib
import time
import csv


def main():

    # Selecting the database where there are both trento and OSM roads
    db = '../db.sqlite'
    connection = sqlite3.connect(db)
    connection.row_factory = sqlite3.Row
    connection.enable_load_extension(True)
    cursor = connection.cursor()
    
    start_time = time.time()
    
    # Selecting all the streets that intersect using a SpatialIndec for better performance
    query = """SELECT osm.name as via_osm, pro.desvia as via_pro 
                    FROM roads_osm as osm, roads_prov as pro 
                    WHERE osm.ROWID IN (SELECT ROWID
                    FROM SpatialIndex
                    WHERE f_table_name = 'roads_osm'
                    AND search_frame = buffer(pro.Geometry, 2.5))
                    AND (via_osm != "" and via_pro != "")
                    ORDER BY via_osm desc"""
    
    cursor.execute(query)
    
    vie = cursor.fetchall()

    end_time = time.time()
    print "Tempo impiegato : ", end_time - start_time
    start_time = time.time()

    to_file_all(vie)
    
    end_time = time.time()
    print "Tempo impiegato : ", end_time - start_time

    connection.close()
    
### This function takes all streets and writes to file all for future refining 
def to_file_all(vie):
    
    vv = list()
    
    # Getting the streets I have already in the other file, to have not copies
    with open("vie_comune_osm.csv") as f:
        filereader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for r in filereader:
            vv.append(r[0])
    
    print vv
    
    # Selecting the second file where are going the other street names
    # ! THE CONTENT OF vie_comune_osm_ver2.csv WILL BE APPENDED BY HAND TO vie_comune_osm.csv FILE
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
        
        # Checking if the street name is already in the other file
        if (via["via_pro"] not in vv):
            if (via_prov == via_osm):
                filewriter.writerow([via["via_pro"].encode('utf8'), via["via_osm"].encode('utf8')])
                vv.append(via["via_pro"])
            elif (last_via_osm == last_via_prov and sm_ratio > 0.65):
                filewriter.writerow([via["via_pro"].encode('utf8'), via["via_osm"].encode('utf8')])
                vv.append(via["via_pro"])

    csvfile.close()

if __name__ == "__main__":
    main()
