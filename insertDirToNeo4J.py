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
    
    if os.path.getsize(dir_choose + '/che.csv') == 0:
        che = []
    else:
        che = pd.read_csv(dir_choose + '/che.csv',header=None,dtype={0:np.object})[0].tolist()
    #print('che',che)
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
    #edges.columsrename(columns={'Claim ID':'Target','损失车辆号牌号码':'Source'})=['Source','Target']
##    for idx,edge in edges.iterrows():
##        #source = edge[0]
##        #target = edge[1]
##
##        sourceType='LostCar'
##        
##        if edge[0] in che:
##            sourceType = 'Car'
##
##        targetType = 'Owner'
##        #relType = 
##
##        if edge[1] in toubaoren:
##            targetType = 'Payer'
##        elif edge[1] in jiashiyuan:
##            targetType = 'Driver'
##        elif edge[1] in lipei:
##            targetType = 'Claim'
##
##        source = Node(sourceType,name=edge[0],gid=gid)
##        target = Node(targetType,name=edge[1],gid=gid)
##        rel = Relationship(source,'rel',target)
##        graph.create(rel)

        
        
    G=nx.from_pandas_edgelist(edges,0,1)
    points=dict()
    node_color = []
    for n in G.nodes():
        if n in che :
            points[n]=Node('Car',code=n,gid=gid)
        elif n in chezhu:
            points[n]=Node('Owner',code=n,gid=gid)
        elif n in toubaoren:
            points[n]=Node('Payer',code=n,gid=gid)
        elif n in jiashiyuan:
            points[n]=Node('Driver',code=n,gid=gid)
        elif n in lipei:
            points[n]=Node('Claim',code=n,gid=gid)
        elif n in sunshiche:
            points[n]=Node('LostCar',code=n,gid=gid)
        else:
            points[n]=Node('Unknown',code=n,gid=gid)
    
    for edge in G.edges():
        graph.create(Relationship(points[edge[0]],'rel',points[edge[1]]))
    
##
##    nx.draw_spring(G,node_color=node_color,with_labels=True)
##    plt.show()

