#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 17:20:35 2021

@author: erikestebanramirezramos
"""

import glob
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

#Open nlloc files (phase readings/phaselink)
nlloc=glob.glob("all_nll_loc/*.hyp")
nlloc=sorted(nlloc)

mv_pol=Polygon([(-115.1136,30.5864),(-116.2621,33.5302),
                (-114.0966,33.5302),(-113.5063,30.5864)])

id5=49999
with open("evlist_phaselink_nlloc_MV.in","w") as file:
    for i in nlloc: # *nlloc files loop
        f=open(i,'r')
        lines=f.readlines()
        lines=lines[7]
        
        year=lines.split()[2]
        month=lines.split()[3]
        day=lines.split()[4]
        hour=lines.split()[5]
        minute=lines.split()[6]
        sec=lines.split()[7]

        lat=lines.split()[9]
        lon=lines.split()[11]
        depth=lines.split()[13]        
        
        id5=id5+1
        
        ############    Polygon Specification     ########################
        epicenter=Point(float(lon),float(lat))
        
        if mv_pol.contains(epicenter)==bool('True'):
            nyear=year
            nmonth=str(month).zfill(2)
            nday=str(day).zfill(2)
            # hour, minute, second=time[j].split(':')
            
            nhour=str(hour).zfill(2)
            nminute=str(minute).zfill(2)
            nsecond=str(sec[0:6]).ljust(6, '0')
    
            nlat=str(lat[:8])
            nlon=str(lon[:10])
            ndepth=str(depth[:6])
            
            file.write("     "+str(id5)+" "+str(nyear)+" "+str(nmonth)+" "
                        +str(nday)+" "+str(nhour)+" "+str(nminute)+" "+
                        str(nsecond)+"  "+nlat+"  "+nlon+"  "+
                        ndepth+"  0.00\n")
        
        