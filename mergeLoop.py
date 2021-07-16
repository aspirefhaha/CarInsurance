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

outdir='fraud_data0602'

loop = pd.read_csv(outdir + r'/loop.csv',encoding='utf8')

suslipei = pd.read_csv(outdir + r'/理赔定损问题_tmp.csv',encoding='utf8')

sus = suslipei.drop_duplicates()


col_name = loop.columns.tolist()
col_name.insert(6,r'注销数量')
col_name.insert(7,r'拒赔数量')
col_name.insert(8,r'注销拒赔数量')
loop = loop.reindex(columns=col_name)

##loop[:,6:8]=0
for ai in range(len(loop)):
##    loop.iloc[ai,r'注销数量'] = 0
##    loop.iloc[ai,r'拒赔数量'] = 0
##    loop.iloc[ai,r'注销拒赔数量'] = 0
    nc = int(loop.loc[ai,r'节点数'])
    ni = int(loop.loc[ai,r'编号'])
    sublipeiname = outdir + '/partitions/' +str(nc) + '/' + str(ni) + '/' + r'理赔信息表.csv'
    sublipei = pd.read_csv(sublipeiname,encoding='utf8',dtype={0:np.object,6:np.object,7:np.object,12:np.object,14:np.object,15:np.object})
    zhuxiaoc = len(sublipei[(sublipei[r'案件状态']==r'注销')])
    jupeic = len(sublipei[(sublipei[r'案件状态']==r'拒赔')])
    loop.iloc[ai,6] = int(zhuxiaoc)
    loop.iloc[ai,7] = int(jupeic)
    loop.iloc[ai,8] = int(zhuxiaoc + jupeic)
    
meg = pd.merge(loop,sus,how='left',left_on=[r'编号',r'节点数'],right_on=[r'编号',r'节点数']).drop_duplicates()
meg.to_csv(outdir + r'/loop合并.csv',sep=',',index=False)
        
