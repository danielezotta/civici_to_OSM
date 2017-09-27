#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 11:32:28 2017

@author: daniele
"""

import sqlite3
import csv

def main():
    
    db = '../db.sqlite'
    connection = sqlite3.connect(db)
    connection.row_factory = sqlite3.Row
    connection.enable_load_extension(True)
    cursor = connection.cursor()
    cursor.execute('SELECT load_extension("mod_spatialite")')
    
    with open("civici_comuni_refined.csv") as f:
        filereader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        f.readline()
        for r in filereader:
            cursor.execute("DELETE FROM civici_prov_principali WHERE PK_UID = " + r[0])
            connection.commit()
            
    connection.close()
    
if __name__ == "__main__":
    main()
