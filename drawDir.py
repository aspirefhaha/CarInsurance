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

#dir_choose = QFileDialog.getExistingDirectory(None,'选取文件夹',os.getcwd())

#if dir_choose == "":
#    sys.exit(0)

while True:
    dir_choose = filedialog.askdirectory()
    if dir_choose == "":
        sys.exit(0)

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
    #print('edges',edges)
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

