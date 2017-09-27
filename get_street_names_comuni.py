#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 10:21:11 2017

@author: daniele
"""

import csv
import sqlite3
import time

def main():
    
    db = '../db.sqlite'
    connection = sqlite3.connect(db)
    connection.row_factory = sqlite3.Row
    connection.enable_load_extension(True)
    cursor = connection.cursor()
    cursor.execute('SELECT load_extension("mod_spatialite")')
    
    start_time = time.time()
    
    csvfile = open("vie_comune_osm.csv", "w")
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(["Via comune", "Via osm"])

    nn = list()

    with open("civici_comuni.csv") as f:
        filereader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        f.readline()
        for r in filereader:
            if r[2] not in nn:
                q = "SELECT desvia FROM civici_prov WHERE pk_uid = " + str(r[0])
                cursor.execute(q)
                rs = cursor.fetchone()
                if rs != None:
                    filewriter.writerow([rs["desvia"], r[4]])
                    nn.append(r[2])
    
    end_time = time.time()
    print "Tempo impiegato : ", end_time - start_time


    
if __name__ == "__main__":
    main()
