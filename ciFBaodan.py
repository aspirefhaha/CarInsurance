# -*-encoding:utf-8 -*-
#/usr/bin/python3
import pandas as pd
import numpy as np
import os

outdir= r'./过滤后数据/'
badoutdir = r'./过滤掉数据/'
indir = r'./'

#def ciFilter(filename,outdir,badoutdir,indir):
isExists = os.path.exists(outdir)
if not isExists:
    os.makedirs(outdir)

isExists = os.path.exists(badoutdir)
if not isExists:
    os.makedirs(badoutdir)

converters = {r'投保人证件号': str,r'被保人证件号':str}

baodandata = pd.read_excel(indir + r'保单信息.xlsx',converters=converters)
                           #dtype=str)

print(r'原始数据大小：',len(baodandata))

chezhuzhengjianhao = baodandata[(baodandata[r'车主姓名'] == baodandata[r'被保人姓名']) & \
                                (baodandata[r'车主证件号'] != baodandata[r'被保人证件号'])]
print(r'车主证件不一致问题数据大小：',len(chezhuzhengjianhao))

for index, row in chezhuzhengjianhao.iterrows():
    baodandata.loc[index,r'车主证件号'] = baodandata.loc[index,r'被保人证件号']

toubaorenzhengjianhao = baodandata[(baodandata[r'投保人姓名'] == baodandata[r'被保人姓名']) & \
                                   ( baodandata[r'投保人证件号'] != baodandata[r'被保人证件号'])]

for index, row in toubaorenzhengjianhao.iterrows():
    baodandata.loc[index,r'投保人证件号'] = baodandata.loc[index,r'被保人证件号']
    baodandata.loc[index,r'投保人姓名'] = baodandata.loc[index,r'被保人姓名']

print(r'投保人证件不一致数据大小：',len(toubaorenzhengjianhao))

chezhuwentibaodan = baodandata[(baodandata[r'车主证件号'].str.len() < 4) |
                               pd.isna(baodandata[r'车主证件号']) |
                               (baodandata[r'车主证件号'].str.match(r'(\w)(\1){3,}'))]

chezhuwentibaodan.to_csv(badoutdir + r'保单信息_车主证件号码问题数据.csv',index=False)
print(r'车主证件号问题数据大小：',len(chezhuwentibaodan))
for index, row in chezhuwentibaodan.iterrows():
    baodandata.loc[index,r'车主证件号'] = ''

toubaorenwentibaodan = baodandata[(baodandata[r'投保人证件号'].str.len() <4) |
                                   pd.isna(baodandata[r'投保人证件号']) |
                                  (baodandata[r'投保人证件号'].str.match(r'(\w)(\1){3,}'))]
toubaorenwentibaodan.to_csv(badoutdir + r'保单信息_投保人证件号码问题数据.csv')
print(r'投保人证件号问题数据大小：',len(toubaorenwentibaodan))
for index, row in toubaorenwentibaodan.iterrows():
    baodandata.loc[index,r'投保人证件号'] = ''

baodandata.to_csv(outdir + r'保单信息.csv',index=False)

#baodandata.dropna(subset=[r'驾驶员证件号码'],inplace=True)
#baodandata[(chesundata[r'驾驶员证件号码'].str.match(r'(\w)(\1){3,}'))]\
#               .to_csv(badoutdir + r'车损信息_证件号码连续四个相同的.csv',index=False)
#baodandata[~ (chesundata[r'驾驶员证件号码'].str.match(r'(\w)(\1){2,}'))]\
#               .to_csv(outdir + r'车损信息.csv',index=False)
