# -*-encoding:utf-8 -*-
#/usr/bin/python3

import pandas as pd
import numpy as np
import os

outdir= r'./过滤后数据/'
badoutdir = r'./过滤掉数据/'
indir = r'./'

isExists = os.path.exists(outdir)
if not isExists:
    os.makedirs(outdir)

isExists = os.path.exists(badoutdir)
if not isExists:
    os.makedirs(badoutdir)

chesundata = pd.read_excel(indir + r'车损信息.xlsx',\
                           dtype={0:object,1:object,r'驾驶员证件号码':object,8:object,9:object,10:object})
chesundata.dropna(subset=[r'驾驶员证件号码'],inplace=True)
chesundata[(chesundata[r'驾驶员证件号码'].str.match(r'(\w)(\1){3,}'))].to_csv(badoutdir + r'车损信息_证件号码连续四个相同的.csv')
chesundata[~ (chesundata[r'驾驶员证件号码'].str.match(r'(\w)(\1){2,}'))].to_csv(outdir + r'车损信息.csv')

#chesundata.to_csv(outdir+r'车损信息.csv',encoding='utf-8-sig',sep=',',index=False)
