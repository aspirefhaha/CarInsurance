# -*-encoding:utf-8 -*-
#/usr/bin/python3
import pandas as pd
import numpy as np
import os

outdir= r'./Filtered/'
badoutdir = r'./过滤掉数据/'
indir = r'./zbx/'

#def ciZBXRenshangFilter(filename,outdir,badoutdir,indir):
isExists = os.path.exists(outdir)
if not isExists:
    os.makedirs(outdir)

isExists = os.path.exists(badoutdir)
if not isExists:
    os.makedirs(badoutdir)

converters = {r'理赔ID': str,r'伤亡人员证件号码':str}

renshangdata = pd.read_excel(indir + r'人员伤亡情况表.xlsx',converters=converters)
                           #dtype=str)


print(r'原始人伤数据大小：',len(renshangdata))
renshangdata =  renshangdata.dropna(subset=[r'理赔ID',r'伤亡人员证件号码',r'人员属性'])
print(r'去除空数据后人伤大小：',len(renshangdata))
renshangdata.to_csv(outdir + r'renshang.csv',index=False,encoding='utf-8')
