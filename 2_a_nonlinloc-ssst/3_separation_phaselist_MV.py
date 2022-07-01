#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 17:20:35 2021

@author: erikestebanramirezramos
"""

import glob
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import shutil

#Open nlloc files (phase readings/phaselink)
nlloc=glob.glob("all_nll_loc/*.hyp")
nlloc=sorted(nlloc)

mv_pol=Polygon([(-115.1136,30.5864),(-116.2621,33.5302),
                (-114.0966,33.5302),(-113.5063,30.5864)])


for i in nlloc: # *nlloc files loop
    f=open(i,'r')
    lines=f.readlines()
    lines=lines[7]

    lat=lines.split()[9]
    lon=lines.split()[11]
    depth=lines.split()[13]        

    
    ############    Polygon Specification     ########################
    epicenter=Point(float(lon),float(lat))
    path, original=i.split('/')
    if mv_pol.contains(epicenter)==bool('True'):
        target=str('MV/'+original)
        shutil.copy(i,target)

        
        