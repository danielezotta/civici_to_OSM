#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 14:20:26 2017

@author: daniele
"""

import csv

def main():

    nn = list()
    
    with open("civici_comuni.csv") as f:
        filereader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for r in filereader:
            nn.append(r[1])
            
    with open("civici_comuni_refined.csv") as f:
        filereader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for r in filereader:
            nn.append(r[1])

    csvfile = open("civici_non_comuni.csv", "w")
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    with open("civici_osm.csv") as f:
        filereader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for r in filereader:
            if r[0] not in nn:
                filewriter.writerow([r[0],r[1],r[2],r[3],r[4]])
        
    print len(nn)


if __name__ == "__main__":
    main()
