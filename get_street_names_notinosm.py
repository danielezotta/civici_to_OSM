#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 12:30:50 2017

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
import time
import csv


def main():

     # Selecting the database where there are both trento and OSM roads
    db = '../db.sqlite'
    connection = sqlite3.connect(db)
    connection.row_factory = sqlite3.Row
    connection.enable_load_extension(True)
    cursor = connection.cursor()
    cursor.execute('SELECT load_extension("mod_spatialite")')
    
    start_time = time.time()
    
    vv = list()
    
    # Selecting the file containing the streets previously estracted
    # ! PLEASE LOOK IN THE to_file_all FUNCTION INSIDE get_street_names BEFORE 
    with open("vie_comune_osm.csv") as f:
        filereader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for r in filereader:
            vv.append(str(r[0]))
    
    cursor.execute("""SELECT *,
                   Y(Transform(Geometry, 4326)) AS LAT,
                   X(Transform(Geometry, 4326)) AS LON
                   FROM civici_prov_principali""")
    
    civici = cursor.fetchall()

    end_time = time.time()
    print "Tempo impiegato : ", end_time - start_time
    start_time = time.time()

    nn = list()
    cc = list()

    # Getting into the command line streets (and LAT, LON for checking) that haven't a corrispondent in OSM
    for civico in civici:
        via_prov = str(civico["desvia"])
        if via_prov not in vv:
            if civico["desvia"] not in nn:
                nn.append(civico["desvia"]) 
                cc.append((civico["LAT"], civico["LON"]))
            
            
    for r in range(0, len(nn)): 
        print nn[r], str(cc[r])
    end_time = time.time()
    print "Tempo impiegato : ", end_time - start_time

    connection.close()

if __name__ == "__main__":
    main()
