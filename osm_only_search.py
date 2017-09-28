#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 14:20:26 2017

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
