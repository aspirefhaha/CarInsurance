# -*-encoding:utf-8 -*-
#/usr/bin/python3

import pandas as pd
import numpy as np
import community
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import scipy
import time
import datetime
import os
import csv
import codecs

datadir1=r'D:/Code/CarInsurance.WithData/Data/zhongbaoxin/out/nodes'
datadir2=r'D:/Code/CarInsurance.WithData/Data/fraud_data0602/nodes'

# Data 1

data1chezhufilename = datadir1 + r'/chezhu.csv'
data1jiashiyuanfilename = datadir1 + r'/jiashiyuan.csv'
data1toubaorenfilename = datadir1 + r'/toubaoren.csv'

data1chefilename = datadir1 + r'/che.csv'
data1sunshichefilename = datadir1 + r'/sunshiche.csv'

# ren
data1chezhu = pd.read_csv(data1chezhufilename,encoding='utf8')
data1chezhu.columns=[r'人']
data1jiashiyuan = pd.read_csv(data1jiashiyuanfilename,encoding='utf8')
data1jiashiyuan.columns=[r'人']
data1toubaoren = pd.read_csv(data1toubaorenfilename,encoding='utf8')
data1toubaoren.columns=[r'人']

# che
data1che = pd.read_csv(data1chefilename,encoding='utf8')
data1che.columns=[r'车']
data1sunshiche = pd.read_csv(data1sunshichefilename,encoding='utf8')
data1sunshiche.columns=[r'车']


data1ren = pd.concat([data1chezhu,data1jiashiyuan,data1toubaoren],
                     keys=[r'人',r'人',r'人'])

data1che = pd.concat([data1che,data1sunshiche])

data1renstat = pd.DataFrame(data1ren.value_counts().reset_index())
data1renstat.columns=[r'人',r'次数']
data1renstat.to_csv(r'./data1ren.csv',sep=',',index=False)

data1chestat = pd.DataFrame(data1che.value_counts().reset_index())
data1chestat.columns=[r'车',r'次数']
data1chestat.to_csv(r'./data1che.csv',sep=',',index=False)

# Data 2

data2chezhufilename = datadir2 + r'/chezhu.csv'
data2jiashiyuanfilename = datadir2 + r'/jiashiyuan.csv'
data2toubaorenfilename = datadir2 + r'/toubao.csv'
data2shangzhefilename = datadir2 + r'/shangzhe.csv'

data2chefilename = datadir2 + r'/che.csv'


# ren 
data2chezhu = pd.read_csv(data2chezhufilename,encoding='utf8')
data2chezhu.columns=[r'人']
data2jiashiyuan = pd.read_csv(data2jiashiyuanfilename,encoding='utf8')
data2jiashiyuan.columns=[r'人']
data2toubaoren = pd.read_csv(data2toubaorenfilename,encoding='utf8')
data2toubaoren.columns=[r'人']
data2shangzhe = pd.read_csv(data2shangzhefilename,encoding='utf8')
data2shangzhe.columns=[r'人']

# che
data2che = pd.read_csv(data2chefilename,encoding='utf8')
data2che.columns=[r'车']

data2ren = pd.concat([data2chezhu,data2jiashiyuan,data2toubaoren,data2shangzhe],
                     keys=[r'人',r'人',r'人',r'人'])

data2renstat = pd.DataFrame(data2ren.value_counts().reset_index())
data2renstat.columns=[r'人',r'次数']
data2renstat.to_csv(r'./data2ren.csv',sep=',',index=False)

data2chestat = pd.DataFrame(data2che.value_counts().reset_index())
data2chestat.columns=[r'车',r'次数']
data2chestat.to_csv(r'./data2che.csv',sep=',',index=False)


statrenout = pd.merge(data1renstat,data2renstat,how='outer',on=r'人')

statrenout.to_csv(r'./dataren.csv',sep=',',index=False)


statcheout = pd.merge(data1chestat,data2chestat,how='outer',on=r'车')

statcheout.to_csv(r'./datache.csv',sep=',',index=False)

print(r'中保信人数：',len(data1renstat))
print(r'华安人数：',len(data2renstat))
print(r'合并人数：',len(statrenout),r'都出现过的人：',len(data1renstat) + len(data2renstat) - len(statrenout))

print(r'中保信车数：',len(data1chestat))
print(r'华安车数：',len(data2chestat))
print(r'合并车数：',len(statcheout),r'都出现过的车：',len(data1chestat) + len(data2chestat) - len(statcheout))

statrenout[(pd.notnull(statrenout[r'次数_x'])&pd.notnull(statrenout[r'次数_y']))].to_csv(r'./中保信和华安都出险过的人.csv',header=False,sep=',')
statcheout[(pd.notnull(statcheout[r'次数_x'])&pd.notnull(statcheout[r'次数_y']))].to_csv(r'./中保信和华安都出险过的车.csv',header=False,sep=',')
