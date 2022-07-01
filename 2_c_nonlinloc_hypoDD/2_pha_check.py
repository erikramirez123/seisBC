#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  3 17:27:14 2022

@author: erikestebanramirezramos
"""
import glob
import collections

file=glob.glob('*.pha')
file=file[0]

f=open(file,'r')


#Preparación para buscar #
idd=[]
index=1
for line in f:
    if '#' in line:
        idd.append(index)
    index+=1
f.close()

#Loop de extracción de id para ver si no es repetido
nid=[]
for i in range(len(idd)):
    # name=name_file(file,idd[i])
    f=open(file,'r')
    info=f.readlines()[int(idd[i])-1]
    element=info.split()[-1]
    print(element)
    nid.append(element)

repeated=[item for item, count in collections.Counter(nid).items() if count > 1]

print('\n')
print('\n')
print('\n')
print('\n')

print(repeated)
