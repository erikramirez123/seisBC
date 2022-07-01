#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 18:55:32 2021

@author: erikestebanramirezramos
"""

import glob
from obspy import read
import datetime
import shutil
import os

pwd=os.getcwd()

archz=glob.glob("20*")
archz=sorted(archz)

for i in range(len(archz)):
    st=read(archz[i])
    
    ntwk=st[0].stats.network
    stcn=st[0].stats.station
    chann=st[0].stats.channel
    
    # #modify BH* into HH*
    # list1=list(chan)
    # list1[0]='H'
    # chann=''.join(list1)
    # st[0].stats.channel=chann
    
    
    year=st[0].stats.starttime.strftime("%Y")
    nzjd=st[0].stats.starttime.strftime("%j")
    
    if len(str(nzjd)) == 1:
        nzjd=str('00'+str(nzjd))
    elif len(str(nzjd)) == 2:
        nzjd=str('0'+str(nzjd))
    else:
        nzjd=nzjd
        
    st.write(str(ntwk)+'.'+str(stcn)+'..'+str(chann)+'.D.'+str(year)+'.'+str(nzjd), format='SAC')
    #st.write(str(ntwk)+'.'+str(stcn)+'..'+str(chann)+'.D.'+str(year)+'.'+str(nzjd), format='MSEED')
    print(str(i)+'_out_'+str(len(archz)))

    #Moving files
    new_file=str(str(ntwk)+'.'+str(stcn)+'..'+str(chann)+'.D.'+str(year)+'.'+str(nzjd))

    shutil.move(str(pwd+'/'+archz[i]), str(pwd+'/orig/'+archz[i]))
    shutil.move(str(pwd+'/'+new_file), str(pwd+'/new/'+new_file))
    