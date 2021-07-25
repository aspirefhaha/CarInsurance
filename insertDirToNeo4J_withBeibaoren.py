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
import sys
import tkinter as tk
from tkinter import filedialog
from py2neo import Node,Relationship,Graph
import re

#dir_choose = QFileDialog.getExistingDirectory(None,'选取文件夹',os.getcwd())

#if dir_choose == "":
#    sys.exit(0)

graph = Graph('http://172.16.155.249:7474',auth=('neo4j','zhu88jie'))
if True:
    dir_choose = filedialog.askdirectory()
    if dir_choose == "":
        sys.exit(0)

    sname = re.split(r'[/|\\]',dir_choose)
    gid=sname[-1]
    gid = 'beibao_' + gid 
    print('gid',gid)
    if os.path.getsize(dir_choose + '/che.csv') == 0:
        che = []
    else:
        che = pd.read_csv(dir_choose + '/che.csv',header=None,dtype={0:np.object})[0].tolist()
    #print('che',che)

    if os.path.getsize(dir_choose + '/beibaoren.csv') == 0:
        beibaoren = []
    else:
        beibaoren = pd.read_csv(dir_choose + '/beibaoren.csv',header=None,dtype={0:np.object})[0].tolist()
    if os.path.getsize(dir_choose + '/chezhu.csv') == 0:
        chezhu = []
    else:
        chezhu = pd.read_csv(dir_choose + '/chezhu.csv',header=None,dtype={0:np.object})[0].tolist()
    #print('chezhu',chezhu)
    if os.path.getsize(dir_choose + '/jiashiyuan.csv') == 0:
        jiashiyuan = []
    else:
        jiashiyuan = pd.read_csv(dir_choose + '/jiashiyuan.csv',header=None,dtype={0:np.object})[0].tolist()
    #print('jiashiyuan',jiashiyuan)
    if os.path.getsize(dir_choose + '/lipei.csv') == 0:
        lipei = []
    else:
        lipei = pd.read_csv(dir_choose + '/lipei.csv',header=None,dtype={0:np.object})[0].tolist()
    #print('lipei',lipei)
    if os.path.getsize(dir_choose + '/sunshiche.csv') == 0:
        sunshiche = []
    else:
        sunshiche = pd.read_csv(dir_choose + '/sunshiche.csv',header=None,dtype={0:np.object})[0].tolist()
    #print('sunshiche',sunshiche)
    if os.path.getsize(dir_choose + '/toubaoren.csv') == 0:
        toubaoren = []
    else:
        toubaoren = pd.read_csv(dir_choose + '/toubaoren.csv',header=None,dtype={0:np.object})[0].tolist()

    
    edges = pd.read_csv(dir_choose + '/edges.csv',sep=' ',header=None,dtype={0:np.object,1:np.object})


    G=nx.from_pandas_edgelist(edges,0,1)
    points=dict()
    node_color = []
    for n in G.nodes():
        if n in che :
            points[n]=Node(r'车',name=r'车'+n,code=n,gid=gid)
        elif n in chezhu:
            points[n]=Node(r'车主',name=r'车主'+n,code=n,gid=gid)
        elif n in toubaoren:
            points[n]=Node(r'投保人',name=r'投保人'+n,code=n,gid=gid)
        elif n in beibaoren:
            points[n]=Node(r'被保人',name=r'被保人'+n,code=n,gid=gid)
        elif n in jiashiyuan:
            points[n]=Node(r'驾驶员',name=r'驾驶员'+n,code=n,gid=gid)
        elif n in lipei:
            points[n]=Node(r'理赔',name=r'理赔'+n,code=n,gid=gid)
        elif n in sunshiche:
            points[n]=Node(r'三者车',name=r'三者车'+n,code=n,gid=gid)
        else:
            points[n]=Node('Unknown',code=n,gid=gid)
    
    for edge in G.edges():
        graph.create(Relationship(points[edge[0]],' ',points[edge[1]]))
    


