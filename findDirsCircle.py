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
import re

if not os.path.exists('./loops'):
    os.makedirs('./loops')


seldir = filedialog.askdirectory()
if seldir == "":
    sys.exit(0)
for dir_choose,dirs,files in os.walk(seldir):
    if not dirs:
        print('root',dir_choose)

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
        ##plt.show()
        ##plt.savefig(dir_choose + '/figure.png')
        hasLoop = False

        try:
            f1 = nx.algorithms.find_cycle(G)
            if f1:
                hasLoop = True
        except:
            pass

        if hasLoop:
            names=re.split(r'[\\|/]',dir_choose)[-2:]
            plt.savefig('./loops/' + names[0] + '_' + names[1] + '.png')
        
        
        plt.clf()
        ##nx.draw_spring(G,node_color=node_color)
        ##plt.savefig(dir_choose + '/figure_nolabel.png')
        ##plt.clf()

