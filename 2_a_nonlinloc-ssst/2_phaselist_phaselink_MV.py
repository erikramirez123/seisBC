#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 17:20:35 2021

@author: erikestebanramirezramos
"""

import glob
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from obspy import UTCDateTime

#Open nlloc files (phase readings/phaselink)
nlloc=glob.glob("all_nll_loc/*.hyp")
nlloc=sorted(nlloc)

######### File to extract the correct ID of the event --------------
evlist=open('evlist_phaselink_nlloc_PRBC.in','r')
evlis_file='evlist_phaselink_nlloc_MV.in'

idd=np.loadtxt(evlis_file,usecols=(0,), dtype=int)
YYYY=np.loadtxt(evlis_file,usecols=(1,), dtype=int)
MMMM=np.loadtxt(evlis_file,usecols=(2,), dtype=int)
DDDD=np.loadtxt(evlis_file,usecols=(3,), dtype=int)
hhhh=np.loadtxt(evlis_file,usecols=(4,), dtype=int)
mmmm=np.loadtxt(evlis_file,usecols=(5,), dtype=int)
ssss=np.loadtxt(evlis_file,usecols=(6,), dtype=float)
ssee, ddee=divmod(ssss,1)



### PRBC Polygon -----------------------------------------------------
prbc_pol = Polygon([(-117.6575, 30.5864), (-118.6947, 33.5302), 
                   (-116.2621, 33.5302), (-115.1136,30.5864)])

# id5=9999
with open("phaselist_phaselink_nlloc_MV.in","w") as file:
    
    ##### event list loop    ==========================
    for evl in range(len(idd)):
        print(evl)
        ms=str(str(int(ddee[evl]*1000000))[:2]+'0000')
        ss_ss=ssss[evl]
        MMMM_M=str(MMMM[evl]).zfill(2)
        DDDD_D=str(DDDD[evl]).zfill(2)
        hhhh_h=str(hhhh[evl]).zfill(2)
        mmmm_m=str(mmmm[evl]).zfill(2)
        ssss_s=str(ss_ss).ljust(6,"0")
        # evlis_time=UTCDateTime(YYYY[evl], MMMM[evl], DDDD[evl], hhhh[evl],
        #                         mmmm[evl], int(ssee[evl]), int(ms))
        evlis_time=str(str(YYYY[evl])+'-'+str(MMMM_M)+'-'+str(DDDD_D)
                    +'-'+str(hhhh_h)+'-'+str(mmmm_m)+'-'+str(ssss_s))
        
        
        ######## *nlloc files loop   ========================
        for i in nlloc: 
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
            
            ########### PRBC   Polygon #########################
            epicenter=Point(float(lon),float(lat))
            
            #####  Phase file time ##################
            # se, de=divmod(float(sec),1)
            # milisec=str(str(int(str(int(de*1000000))[:2]))+'0000')
            # phase_time=UTCDateTime(int(year), int(month), int(day), int(hour),
            #                         int(minute), int(float(sec)),int(milisec))
            phase_time=str(str(year)+'-'+str(month)+'-'+str(day)+'-'+str(hour)
                            +'-'+str(minute)+'-'+str(sec[:6]))
        
            if evlis_time==phase_time:
                # print(phase_time)
                # print(evlis_time)
                # print(idd[evl])
                # print('===========')
                ID=idd[evl]

            # #########  Asking if epicenter in inside the PRBC polygon   ######## 
            # if prbc_pol.contains(epicenter)==bool('True'):
                # id5=id5+1 ####### ID issue +++++++++++++++++++++++
    
                nyear=year
                nmonth=str(month).zfill(2)
                nday=str(day).zfill(2)
                
                nhour=str(hour).zfill(2)
                nminute=str(minute).zfill(2)
                nsecond=str(sec[0:6]).ljust(6, '0')
        
                nlat=str(lat[:8])
                nlon=str(lon[:10])
                ndepth=str(depth[:6])
                ############ Location line ####################
                file.write("     "+str(ID)+" "+str(nyear)+" "+str(nmonth)+" "
                            +str(nday)+" "+str(nhour)+" "+str(nminute)+" "+
                            str(nsecond)+"  "+nlat+"  "+nlon+"  "+
                            ndepth+"  0.00\n")
                
                ###############  Reading start and end of phase picks ###############
                with open(i) as fl:
                    # start=0; end=0
                    # Ignore the last (or any) white line #######
                    lins = (line.rstrip() for line in fl) # All lines including the blank ones
                    lins = list(line for line in lins if line) # Non-blank lines in a list
                    
                    # Origin time
                    se, de=divmod(float(sec),1)
                    ot=UTCDateTime(int(year), int(month), int(day), 
                                    int(hour),int(minute), int(float(sec)), int(de*1000000))
                    # print('==========================')
                    for s in range(18,(len(lins)-2)):
                        ln=lins[s]
                        ntwk=ln.split()[1]
                        stcn=ln.split()[0]
                        stcn=str(stcn).ljust(5," ")
                        phase=ln.split()[4]
                        
                        #    DATE/TIME
                        date=ln.split()[6]
                        YY=int(date[:4])
                        MM=int(date[4:6])
                        DD=int(date[6:8])
                        time=ln.split()[7]
                        hh=int(time[:2])
                        mm=int(time[2:4])
                        seconds=ln.split()[8]
                        SE, DE=divmod(float(seconds),1)
                        pht=UTCDateTime(int(YY), int(MM), int(DD), int(hh), int(mm),
                                        int(SE), int(DE*1000000))
                        sec_diff=pht-ot # Arrival time (s)
                        sec_diff=str(sec_diff)[:6]
                        
                        dis=ln.split()[21]
                        dis=str(dis)[:6]
                        
                        file.write(str(ntwk)+" "+str(stcn)+" "+phase+"  "+sec_diff+
                                        "  "+dis+"\n")
                
            
            
            
            
            
            
                
                
                
                
                
                
                
                
                
                
                
                