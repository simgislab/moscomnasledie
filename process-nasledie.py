#!/usr/bin/env python -u
# -*- coding: utf-8 -*-
# vim:et
# ---------------------------------------------------------------------------
# nasledie-processor.py
# Author: Maxim Dubinin (sim@gis-lab.info)
# About: Process html grabbed from http://dkn.mos.ru/contacts/register-of-objects-of-cultural-heritage/memorial/ to csv.
# Created: 20:05 05.02.2014
# Usage example: python nasledie-processor.py
# ---------------------------------------------------------------------------

from bs4 import BeautifulSoup
import sys
import os
import ucsv as csv
import datetime
import time
import glob

def parse_org(id):
    id_data = open(id)
    id = id.replace(".html","")
    soup = BeautifulSoup(''.join(id_data.read()))
    maintable = soup.find("div", { "class" : "feature_list" })

    if str(maintable) == 'None':
        id = name_obj = name_ans = history = history_cat = protection = address = "EMPTY"
        f_errors.write(id + "," + link + ", id is empty" + "\n")
    else:
        spans = maintable.findAll("span")
        
        if len(spans) < 12:
            id = name_obj = name_ans = history = history_cat = protection = address = "ERROR"
            f_errors.write(id + "," + link + ", incorrect data" + "\n")
        else:
            arr = []
            for i in range(12):
                if list(spans[i].strings) != []:
                    arr.append(list(spans[i].strings)[0])
                else:
                    arr.append("")

    #write to results file
    csvwriter.writerow(dict(ID=id,
                            URL=link,
                            NAME_OBJ=arr[1].strip(),
                            NAME_ANS=arr[3].strip(),
                            HISTORY=arr[5].strip(),
                            HISTORY_CAT=arr[7].strip(),
                            PROTECTION=arr[9].strip(),
                            ADDRESS=arr[11].strip()))

if __name__ == '__main__':
    os.chdir("data")
    f_errors = open("../errors.csv","wb")
       
    fieldnames_data = ("ID","URL","NAME_OBJ","NAME_ANS","HISTORY","HISTORY_CAT","PROTECTION","ADDRESS")
    f_data = open("../all_data.csv","wb")
    csvwriter = csv.DictWriter(f_data, fieldnames=fieldnames_data)
    
    
    for id in glob.glob("*.html"):
        link = "http://dkn.mos.ru/contacts/register-of-objects-of-cultural-heritage/memorial/" + id.replace(".html","") + "/"
        print("Processing id " + id)
        parse_org(id)
        
    f_data.close()
    f_errors.close()
