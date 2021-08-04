# -*-encoding:utf-8 -*-
#/usr/bin/python3
import pandas as pd
import numpy as np
import os

outdir= r'./Filtered/'
badoutdir = r'./过滤掉数据/'
indir = r'./zbx/'

#def ciFilter(filename,outdir,badoutdir,indir):
isExists = os.path.exists(outdir)
if not isExists:
    os.makedirs(outdir)

isExists = os.path.exists(badoutdir)
if not isExists:
    os.makedirs(badoutdir)

converters = {r'保单ID': str,r'身份证号':str}

juesedata = pd.read_excel(indir + r'保单角色表.xlsx',converters=converters)
                           #dtype=str)


print(r'原始角色数据大小：',len(juesedata))
juesedata =  juesedata.dropna(subset=[r'保单ID',r'身份证号'])
print(r'去除空数据后角色大小：',len(juesedata))

sfz = juesedata[r'身份证号'].value_counts()
sfz.to_csv(badoutdir + '身份证统计.csv')
sfzstr = '|'.join(sfz[sfz.values>100].index.to_list())
juesedata = juesedata[(~ juesedata[r'身份证号'].str.contains(sfzstr))]
#juesedata = juesedata[(juesedata[r'身份证号']!= 'cfcd208495d565ef66e7dff9f98764da')
#                        & (juesedata[r'身份证号']!= 'd1dee99ac0257b5f6c9df49730478c4c')]
print(r'删除无效身份证号数据后角色大小：',len(juesedata))
#juesedata[[r'身份证号']].groupby(r'身份证号').count().sort_values(by='count',ascending=0).to_csv(badoutdir + 'count.csv')

converters = {r'保单ID': str,r'车架号':str}
baodandata = pd.read_excel(indir + r'保单表.xlsx',converters = converters)
print(r'原始保单数据大小：',len(baodandata))
baodandata = baodandata.dropna(subset=[r'保单ID',r'车架号'])
print(r'去除空数据后保单大小：',len(baodandata))

juesedata.to_csv(outdir + r'juese.csv',index=False,encoding='utf-8')
baodandata.to_csv(outdir + r'baodan.csv',index=False,encoding='utf-8')

#juesedata.dropna(subset=[r'驾驶员证件号码'],inplace=True)
#juesedata[(chesundata[r'驾驶员证件号码'].str.match(r'(\w)(\1){3,}'))]\
#               .to_csv(badoutdir + r'车损信息_证件号码连续四个相同的.csv',index=False)
#juesedata[~ (chesundata[r'驾驶员证件号码'].str.match(r'(\w)(\1){2,}'))]\
#               .to_csv(outdir + r'车损信息.csv',index=False)
