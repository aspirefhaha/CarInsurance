# -*-encoding:utf-8 -*-
#/usr/bin/python3
import pandas as pd
import numpy as np
import os

outdir= r'./Filtered/'
badoutdir = r'./过滤掉数据/'
indir = r'./zbx/'

#def ciZBXChesunFilter(filename,outdir,badoutdir,indir):
isExists = os.path.exists(outdir)
if not isExists:
    os.makedirs(outdir)

isExists = os.path.exists(badoutdir)
if not isExists:
    os.makedirs(badoutdir)

converters = {r'Claim ID ': str,r'车架号':str,r'出险驾驶员证件号码':str}

chesundata = pd.read_excel(indir + r'理赔车损表.xlsx',converters=converters)
                           #dtype=str)


print(r'原始车损数据大小：',len(chesundata))
chesundata =  chesundata.dropna(subset=[r'Claim ID ',r'车架号',r'出险驾驶员证件号码',r'是否承保车辆'])
chesundata = chesundata.rename(columns={r'Claim ID ':r'理赔ID'})
print(r'去除空数据后车损大小：',len(chesundata))
chesundata.to_csv(outdir + r'chesun.csv',index=False,encoding='utf-8-sig')
