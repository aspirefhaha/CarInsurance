# -*-encoding:utf-8 -*-
#/usr/bin/python3

import pandas as pd
import datetime
import numpy as np
import community
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import scipy
import time
import os
import csv
import codecs
import shutil

bothpeople = pd.read_csv(r'D:/Code/CarInsurance.WithData/Data/两家一起/中保信和华安都出险过的人.csv',header=None)
bothcar = pd.read_csv(r'D:/Code/CarInsurance.WithData/Data/两家一起/中保信和华安都出险过的车.csv',header=None)

peoplestr = '|'.join(bothpeople[1].tolist())
carstr = '|'.join(bothcar[1].tolist())

huaandir=r'D:/Code/CarInsurance.WithData/Data/两家一起/原始数据/华安'
zhongbaoxindir=r'D:/Code/CarInsurance.WithData/Data/两家一起/原始数据/中保信'

# 华安 Data
huaanbaodanjuese = pd.read_csv(huaandir + r'/保单角色信息表.csv',encoding='utf8',dtype={0:np.object})
huaanbaodan = pd.read_csv(huaandir + r'/保单信息表.csv',encoding='utf8',dtype={0:np.object,1:np.object})
huaanchesun = pd.read_csv(huaandir + r'/车损信息.csv',encoding='utf8',dtype={0:np.object,3:np.object,5:np.object,8:np.object})
huaanlipei = pd.read_csv(huaandir + r'/理赔信息表.csv',encoding='utf8',dtype={0:np.object,6:np.object,7:np.object,12:np.object,14:np.object,15:np.object})
huaanpeifu = pd.read_csv(huaandir + r'/赔付信息表.csv',encoding='utf8',dtype={0:np.object})
huaanrenshang = pd.read_csv(huaandir + r'/人伤信息.csv',encoding='utf8',dtype={0:np.object})
huaanrenshang.rename(columns={r'理赔id':r'理赔ID'},inplace=True)

huaanlipei = huaanlipei[(huaanlipei[r'出险驾驶员证件号码'].str.contains(peoplestr)) |
                        (huaanlipei[r'车架号'].str.contains(carstr)) |
                        (huaanlipei[r'车主证件号'].str.contains(peoplestr)) ]
lipeistr = '|'.join(huaanlipei[r'理赔ID'].tolist())

huaanbaodanjuese = huaanbaodanjuese[(huaanbaodanjuese[r'被保险人证件号'].str.contains(peoplestr)) |
                                    (huaanbaodanjuese[r'投保人证件号'].str.contains(peoplestr)) |
                                    (huaanbaodanjuese[r'车主证件号'].str.contains(peoplestr))]

baodanidstr = '|'.join(huaanbaodanjuese[r'保单ID'].tolist())
huaanbaodan = huaanbaodan[(huaanbaodan[r'保单ID'].str.contains(baodanidstr)) |
                          (huaanbaodan[r'车架号'].str.contains(carstr))]

huaanchesun = huaanchesun[huaanchesun[r'出险驾驶员证件号码'].str.contains(peoplestr) |
                          huaanchesun[r'车架号'].str.contains(carstr) ]

huaanpeifu = huaanpeifu[ (huaanpeifu[r'理赔ID'].str.contains(lipeistr))]

huaanrenshang = huaanrenshang[ (huaanrenshang[r'理赔ID'].str.contains(lipeistr)) |
                                (huaanrenshang[r'伤者证件号'].str.contains(peoplestr))]

huaanbaodanjuese.to_csv(r'D:/Code/CarInsurance.WithData/Data/两家一起/摘取出数据/华安/保单角色信息表.csv',sep=',',encoding='utf8',index=False)
huaanbaodan.to_csv(r'D:/Code/CarInsurance.WithData/Data/两家一起/摘取出数据/华安/保单信息表.csv',sep=',',encoding='utf8',index=False)
huaanchesun.to_csv(r'D:/Code/CarInsurance.WithData/Data/两家一起/摘取出数据/华安/车损信息.csv',sep=',',encoding='utf8',index=False)
huaanlipei.to_csv(r'D:/Code/CarInsurance.WithData/Data/两家一起/摘取出数据/华安/理赔信息表.csv',sep=',',encoding='utf8',index=False)
huaanpeifu.to_csv(r'D:/Code/CarInsurance.WithData/Data/两家一起/摘取出数据/华安/赔付信息表.csv',sep=',',encoding='utf8',index=False)
huaanrenshang.to_csv(r'D:/Code/CarInsurance.WithData/Data/两家一起/摘取出数据/华安/人伤信息.csv',sep=',',encoding='utf8',index=False)


#中保信 Data
zbxchesun = pd.read_csv(zhongbaoxindir + r'/chesun.csv',encoding='utf8')

zbxlipeibaodan = pd.read_csv(zhongbaoxindir + r'/lipeibaodan.csv',encoding='utf8')

zbxchesun = zbxchesun[ (zbxchesun[r'损失车辆驾驶员'].str.contains(peoplestr)) |
                       (zbxchesun[r'车架号'].str.contains(carstr)) ]

zbxlipeibaodan = zbxlipeibaodan[ (zbxlipeibaodan[r'车架号'].str.contains(carstr)) |
                                 (zbxlipeibaodan[r'投保人'].str.contains(peoplestr)) |
                                 (zbxlipeibaodan[r'被保人'].str.contains(peoplestr)) |
                                 (zbxlipeibaodan[r'车主'].str.contains(peoplestr)) |
                                 (zbxlipeibaodan[r'出险驾驶员证件号码'].str.contains(peoplestr))]
zbxchesun.to_csv(r'D:/Code/CarInsurance.WithData/Data/两家一起/摘取出数据/中保信/chesun.csv',sep=',',encoding='utf8',index=False)
zbxlipeibaodan.to_csv(r'D:/Code/CarInsurance.WithData/Data/两家一起/摘取出数据/中保信/lipeibaodan.csv',sep=',',encoding='utf8',index=False)



