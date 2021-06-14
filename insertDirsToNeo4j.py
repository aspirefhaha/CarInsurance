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

graph = Graph('http://172.16.155.249:7474',auth=('neo4j','zhu88jie'))

seldir = filedialog.askdirectory()
if seldir == "":
    sys.exit(0)
for dir_choose,dirs,files in os.walk(seldir):
    if not dirs:
        print('root',dir_choose)

        sname = re.split(r'[/|\\]',dir_choose)
        gid=sname[-1]

        if not os.path.exists(dir_choose + '/che.csv'):
            continue
        
        if os.path.getsize(dir_choose + '/che.csv') == 0:
            che = []
        else:
            che = pd.read_csv(dir_choose + '/che.csv',header=None,dtype={0:np.object})[0].tolist()

        if os.path.getsize(dir_choose + '/chezhu.csv') == 0:
            chezhu = []
        else:
            chezhu = pd.read_csv(dir_choose + '/chezhu.csv',header=None,dtype={0:np.object})[0].tolist()

        if os.path.getsize(dir_choose + '/jiashiyuan.csv') == 0:
            jiashiyuan = []
        else:
            jiashiyuan = pd.read_csv(dir_choose + '/jiashiyuan.csv',header=None,dtype={0:np.object})[0].tolist()

        if os.path.getsize(dir_choose + '/lipei.csv') == 0:
            lipei = []
        else:
            lipei = pd.read_csv(dir_choose + '/lipei.csv',header=None,dtype={0:np.object})[0].tolist()

        if os.path.getsize(dir_choose + '/sunshiche.csv') == 0:
            sunshiche = []
        else:
            sunshiche = pd.read_csv(dir_choose + '/sunshiche.csv',header=None,dtype={0:np.object})[0].tolist()

        if os.path.getsize(dir_choose + '/toubaoren.csv') == 0:
            toubaoren = []
        else:
            toubaoren = pd.read_csv(dir_choose + '/toubaoren.csv',header=None,dtype={0:np.object})[0].tolist()

        if os.path.getsize(dir_choose + '/edges.csv') == 0:
            continue
        edges = pd.read_csv(dir_choose + '/edges.csv',sep=' ',header=None,dtype={0:np.object,1:np.object})
        #edges.columsrename(columns={'Claim ID':'Target','损失车辆号牌号码':'Source'})=['Source','Target']

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

