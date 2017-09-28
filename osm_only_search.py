#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 14:20:26 2017

@author: daniele
"""

import csv

def main():

    nn = list()
    
    # Opening and reading all the common housenumbers and store into list the primary key
    with open("civici_comuni.csv") as f:
        filereader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for r in filereader:
            nn.append(r[1])
            
    with open("civici_comuni_refined.csv") as f:
        filereader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for r in filereader:
            nn.append(r[1])

    # Selecting the file to write
    csvfile = open("civici_non_comuni.csv", "w")
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    # Writing to file only housenumbers that are into OpenStreetMap and 
    # don't intersects with a municipality's housenumber
    with open("civici_osm.csv") as f:
        filereader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for r in filereader:
            if r[0] not in nn:
                filewriter.writerow([r[0],r[1],r[2],r[3],r[4]])
        
    csvfile.close()


if __name__ == "__main__":
    main()
