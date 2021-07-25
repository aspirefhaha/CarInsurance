# -*-encoding:utf-8 -*-
#/usb/bin/python3

import pandas as pd
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

che = pd.read_csv('./che.csv',header=None,dtype={0:np.object})[0].tolist()

chezhu = pd.read_csv('./chezhu.csv',header=None,dtype={0:np.object})[0].tolist()

jiashiyuan = pd.read_csv('./jiashiyuan.csv',header=None,dtype={0:np.object})[0].tolist()

lipei = pd.read_csv('./lipei.csv',header=None,dtype={0:np.object})[0].tolist()

sunshiche = pd.read_csv('./sunshiche.csv',header=None,dtype={0:np.object})[0].tolist()

if os.path.getsize('./toubaoren.csv') == 0:
    toubaoren = []
else:
    toubaoren = pd.read_csv('./toubaoren.csv',header=None,dtype={0:np.object})[0].tolist()

edges = pd.read_csv('./edges.csv',sep=' ',header=None,dtype={0:np.object})
#edges.columsrename(columns={'Claim ID':'Target','损失车辆号牌号码':'Source'})=['Source','Target']

G=nx.from_pandas_edgelist(edges,0,1)

node_color = []
for n in G.nodes():
    if n in che :
        node_color.append('blue')
    elif n in chezhu:
        node_color.append('green')
    elif n in toubaoren:
        node_color.append('red')
    elif n in jiashiyuan:
        node_color.append('yellow')
    elif n in lipei:
        node_color.append('cyan')
    elif n in sunshiche:
        node_color.append('grey')
    else:
        node_color.append('black')

nx.draw_spring(G,node_color=node_color,with_labels=True)
plt.show()

