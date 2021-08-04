# -*-encoding:utf-8 -*-
#/usr/bin/python3
import pandas as pd
import numpy as np
import os

outdir= r'./Filtered/'
badoutdir = r'./过滤掉数据/'
indir = r'./zbx/'

#def ciZBXZhifuFilter(filename,outdir,badoutdir,indir):
isExists = os.path.exists(outdir)
if not isExists:
    os.makedirs(outdir)

isExists = os.path.exists(badoutdir)
if not isExists:
    os.makedirs(badoutdir)

converters = {r'claimID ': str,r'赔款收款身份证/组织机构代码':str}

zhifudata = pd.read_excel(indir + r'理赔支付.xlsx',converters=converters)
                           #dtype=str)


print(r'原始支付数据大小：',len(zhifudata))
zhifudata = zhifudata.dropna(subset=[r'claimID',r'赔款收款身份证/组织机构代码'])
zhifudata = zhifudata.rename(columns={r'claimID':r'理赔ID',r'赔款收款身份证/组织机构代码':r'收款身份证'})
print(r'去除空数据后支付大小：',len(zhifudata))
zhifudata.to_csv(outdir + r'zhifu.csv',index=False,encoding='utf-8-sig')
