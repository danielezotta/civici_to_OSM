#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 09:16:28 2017

@author: daniele
"""

import sqlite3
import osmapi
import csv
import time


def main():

    db = '../db.sqlite'
    connection = sqlite3.connect(db)
    connection.row_factory = sqlite3.Row
    connection.enable_load_extension(True)
    cursor = connection.cursor()
    cursor.execute('SELECT load_extension("mod_spatialite")')

    api = osmapi.OsmApi(passwordfile="/etc/osmpassword.txt")
    api.ChangesetCreate({u"comment": u"Inserted housenumbers"})

    query = """SELECT *,
            Y(Transform(Geometry, 4326)) AS LAT,
            X(Transform(Geometry, 4326)) AS LON
            FROM civici_prov_principali WHERE desvia = 'VIA A. APOLLONIO'"""
    cursor.execute(query)

    civici = cursor.fetchall()

    for civico in civici:
        
        if (civico["ingresso"] == "cancello"):
            node = {u"lon":round(civico["LON"], 6), u"lat":round(civico["LAT"], 6), u"tag": 
                {u"addr:housenumber":str(civico["civico_alf"]).encode('utf-8'), 
                 u"addr:street":get_via_osm(civico["desvia"]), 
                 u"addr:postcode":str(civico["cap"]).encode('utf-8'), 
                 u"addr:city":str(civico["sobborgo"]).encode('utf-8'), 
                 u"barrier":u"gate"}}
        else:
            node = {u"lon":round(civico["LON"], 6), u"lat":round(civico["LAT"], 6), u"tag": 
                {u"addr:housenumber":str(civico["civico_alf"]).encode('utf-8'), 
                 u"addr:street":get_via_osm(civico["desvia"]), 
                 u"addr:postcode":str(civico["cap"]).encode('utf-8'), 
                 u"addr:city":str(civico["sobborgo"]).encode('utf-8')}}
        
        print api.NodeCreate(node)
        
        cursor.execute("""DELETE FROM civici_prov_principali WHERE PK_UID = """ + str(civico["PK_UID"]))
        connection.commit()

        time.sleep(10)
        
    api.ChangesetClose()

def get_via_osm(via_comune):

    with open("vie_comune_osm.csv") as f:
        filereader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        f.readline()
        for r in filereader:
            if r[0].decode("utf-8") == via_comune:
                return unicode(r[1], 'utf-8')
    f.close()
    return via_comune

def get_via_comune(via_osm):

    with open("vie_comune_osm.csv") as f:
        filereader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        f.readline()
        for r in filereader:
            if r[1] == via_osm:
                return r[0]
    f.close()
    return via_osm

if __name__ == "__main__":
    main()