#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 19 20:15:01 2021

@author: erikestebanramirezramos
"""

import glob
import numpy as np


nlloc_files=glob.glob("all_nll_loc/*.hyp")
nlloc_files=sorted(nlloc_files)

evlis_file='evlist_phaselink_nlloc_prbc_mv.in' ### Ev. list out of nlloc files)
ssst_file='L3_120km_phaselink_loc_ssst_prbc_mv.out' ## Ev. list out of ssst


##### Extract info from event list (compulation of original nlloc files)
iddd_1=np.loadtxt(evlis_file,usecols=(0,), dtype=str)
YYYY_1=np.loadtxt(evlis_file,usecols=(1,), dtype=str)
MMMM_1=np.loadtxt(evlis_file,usecols=(2,), dtype=str)
DDDD_1=np.loadtxt(evlis_file,usecols=(3,), dtype=str)
hhhh_1=np.loadtxt(evlis_file,usecols=(4,), dtype=str)
mmmm_1=np.loadtxt(evlis_file,usecols=(5,), dtype=str)
ssss_1=np.loadtxt(evlis_file,usecols=(6,), dtype=float)
ssee_1, ddee_1=divmod(ssss_1,1)


##### New locations out of the SSST analysis
iddd_2=np.loadtxt(ssst_file,usecols=(0,), dtype=str)
YYYY_2=np.loadtxt(ssst_file,usecols=(1,), dtype=str)
MMMM_2=np.loadtxt(ssst_file,usecols=(2,), dtype=str)
DDDD_2=np.loadtxt(ssst_file,usecols=(3,), dtype=str)
hhhh_2=np.loadtxt(ssst_file,usecols=(4,), dtype=str)
mmmm_2=np.loadtxt(ssst_file,usecols=(5,), dtype=str)
ssss_2=np.loadtxt(ssst_file,usecols=(6,), dtype=float)
ssee_2, ddee_2=divmod(ssss_2,1)
lat_2=np.loadtxt(ssst_file,usecols=(7,), dtype=str)
lon_2=np.loadtxt(ssst_file,usecols=(8,), dtype=str)
dep_2=np.loadtxt(ssst_file,usecols=(9,), dtype=str)


for i in nlloc_files:
    f=open(i,'r')
    Lines=f.readlines()
    lines=Lines[7]
    
    # Read 'Geographyc' line in nlloc file
    year=lines.split()[2]
    month=lines.split()[3]
    day=lines.split()[4]
    hour=lines.split()[5]
    minute=lines.split()[6]
    second=lines.split()[7]
    sec,dsec=divmod(float(second),1)
    latitude=lines.split()[9]
    longitude=lines.split()[11]
    depth=lines.split()[13]
    
    #String of individual nlloc file for idintification
    nlloc_time=[year+' '+month+' '+day+' '+hour+' '+minute+' '+str(sec)]
    
    #id extractor
    for d in range(len(iddd_1)):
        evlist_time=[YYYY_1[d]+' '+MMMM_1[d]+' '+DDDD_1[d]+' '+hhhh_1[d]
                     +' '+mmmm_1[d]+' '+str(ssee_1[d])]
        if nlloc_time==evlist_time:
            ID=iddd_1[d]
    
    # Variables (ssst loc) to replace nlloc variables
    for r in range(len(iddd_2)):
        if ID==iddd_2[r]:
            n_minute=mmmm_2[r].zfill(2)
            n_second=str(ssss_2[r]).ljust(9,'0')
            n_latitude=lat_2[r].ljust(9,'0')
            n_longitude=lon_2[r].ljust(11,'0')
            n_depth=dep_2[r].ljust(9,'0')
    f.close()
    
    # Replace loc variables into nlloc files from ssst locations
    old_data=[minute, second, latitude, longitude, depth]
    new_data=[n_minute, n_second,n_latitude,n_longitude, n_depth]
    
    for nd in range(len(new_data)):
        nf=open(i,'r')
        
        LINES=nf.readlines()
        LINE=LINES[7]
        NF=open(i,'w')
        
        for p in range(7):
            NF.write(LINES[p])
        
        NF.write(LINE.replace(old_data[nd], new_data[nd]))
        for e in range(8,len(LINES)):
            NF.write(LINES[e])
        nf.close()
        NF.close()
    

        

    
    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
