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


print(os.getcwd())

isExists = os.path.exists('./out/partitions')
if not isExists:
    os.makedirs('./out/partitions')

isExists = os.path.exists('./out/edges')
if not isExists:
    os.makedirs('./out/edges')

isExists = os.path.exists('./out/nodes')
if not isExists:
    os.makedirs('./out/nodes')

##juese = pd.read_csv('./samples/juese.csv',sep='\t',encoding='gb18030',header=None,dtype={0:np.object})
##juese.dropna(subset=[0,1,3],inplace=True)
##juese=juese[[0,1,3]]
##juese=juese.drop_duplicates()
##toubao = juese[(juese[1]==2)&(juese[3]!='cfcd208495d565ef66e7dff9f98764da')][[0,3]]
##beibao = juese[(juese[1]==3)&(juese[3]!='cfcd208495d565ef66e7dff9f98764da')][[0,3]]
##chezhu = juese[(juese[1]==4)&(juese[3]!='cfcd208495d565ef66e7dff9f98764da')][[0,3]]
##juese = pd.merge(toubao,beibao,on=0)
##juese = pd.merge(juese,chezhu,on=0)
##juese[0]=juese[0].str.split('.',expand=True)[0].str.strip()
#####print(df.columns.values)
##juese.to_csv('./out/juese.csv',sep=',',header=['保单ID','投保人','被保人','车主'],index=False)
####
##baodan = pd.read_csv('./samples/baodan.csv',
##                     sep='\t',encoding='gb18030',header=None,
##                     dtype={0:np.object})
##
##baodan.dropna(subset=[0,2],inplace=True)
##baodan=baodan[[0,2]]
####baodan[0] = baodan[0].astype('str').str.split('.')[0]
####print(baodan.dtypes)
##baodan=baodan.drop_duplicates()
##baodan[0] =baodan[0].str.split('.',expand=True)[0].str.strip()
##baodan.to_csv('./out/baodan.csv',sep=',',header=['保单ID','车牌'],index=False)
##
##baodanjuese=pd.merge(baodan,juese,on=0)
####baodanjuese[0] = baodanjuese[0].str.split('.',expand=True)[0].str.strip()
##baodanjuese.columns =['保单ID','保单车牌','投保人','被保人','车主']
##baodanjuese.to_csv('./out/juesebaodan.csv',sep=',',index=False)
##
##lipei = pd.read_csv('./samples/lipei.csv',
##                    sep=',',encoding='gb18030',
##                    dtype={'保单ID':np.object,'Claim ID':np.object})
##
##
##lipei.dropna(subset=['Claim ID','保单ID','出险驾驶员证件号码','出险车辆号牌号码','车架号'],inplace=True)
##lipei = lipei[(lipei['车架号']!='cfcd208495d565ef66e7dff9f98764da')]
##lipei = lipei[(lipei['车架号异常']!=0)&(lipei['证件号异常']!=0)]
##lipei=lipei[['Claim ID','保单ID','出险驾驶员证件号码','出险车辆号牌号码']]
##
##lipei=lipei[(lipei['出险驾驶员证件号码']!='cfcd208495d565ef66e7dff9f98764da')]
##
##lipei['is_duplicated']=lipei.duplicated(['Claim ID'])
##lipei_dup = lipei.loc[lipei['is_duplicated']==True]
##lipei_ind = lipei.loc[lipei['is_duplicated']==False]
##lipei_ind.to_csv('./out/lipei_ind.csv',sep=',',index=False)
##lipei_dup.to_csv('./out/lipei_dup.csv',sep=',',index=False)
##
##
##chesun = pd.read_csv('./samples/chesun.csv',sep=',',header=None,encoding='gb18030',dtype={0:np.object})
##
##chesun.dropna(subset=[0,2],inplace=True)
##
##chesun = chesun[[0,2]]
##chesun = chesun[(chesun[2]!= 'a258e8d7a8f4a0e58ffef13d17281a83')]
##
##chesun = chesun.drop_duplicates()
##
##chesun[0] = chesun[0].str.split('.',expand=True)[0].str.strip()
##chesun.columns=['Claim ID','损失车辆号牌号码']
##chesun.to_csv('./out/chesun.csv',sep=',',index=False)
##
##
##lipei = pd.merge(lipei_ind,chesun,on='Claim ID',how='inner')
##lipei.to_csv('./out/lipeichesun.csv',sep=',',index=False)
##
##lipeibaodan = pd.merge(lipei,baodanjuese,on='保单ID',how='inner')
##lipeibaodan = lipeibaodan.drop_duplicates(subset=['Claim ID'])
##lipeibaodan = lipeibaodan[['Claim ID','保单ID','出险车辆号牌号码','保单车牌','投保人','被保人','车主','出险驾驶员证件号码','损失车辆号牌号码']]
##haopaiwentishuju = lipeibaodan[(lipeibaodan['出险车辆号牌号码']!= lipeibaodan['保单车牌'])]
##
##lipeibaodan = lipeibaodan[(lipeibaodan['出险车辆号牌号码']== lipeibaodan['保单车牌'])]
##
##haopaiwentishuju.to_csv('./out/haopaiwentishuju.csv',sep=',',index=False)
##
##lipeibaodan.to_csv('./out/lipeibaodan.csv',sep=',',index=False)

lipeibaodan = pd.read_csv('./out/lipeibaodan.csv')
##lipeibaodan = lipeibaodan.iloc[0:1000,:]

che = lipeibaodan['保单车牌'].drop_duplicates()
sunshiche = lipeibaodan['损失车辆号牌号码'].drop_duplicates()
chezhu=lipeibaodan['车主'].drop_duplicates()
toubaoren=lipeibaodan['投保人'].drop_duplicates()
jiashiyuan=lipeibaodan['出险驾驶员证件号码'].drop_duplicates()
lipei=lipeibaodan['Claim ID'].drop_duplicates()


che.to_csv('./out/nodes/che.csv',sep=',',index=False)
chezhu.to_csv('./out/nodes/chezhu.csv',sep=',',index=False)
toubaoren.to_csv('./out/nodes/toubaoren.csv',sep=',',index=False)
jiashiyuan.to_csv('./out/nodes/jiashiyuan.csv',sep=',',index=False)
lipei.to_csv('./out/nodes/lipei.csv',sep=',',index=False)
sunshiche.to_csv('./out/nodes/sunshiche.csv',sep=',',index=False)

che = che.tolist()
chezhu=chezhu.tolist()
sunshiche = sunshiche.tolist()
toubaoren=toubaoren.tolist()
jiashiyuan=jiashiyuan.tolist()
lipei=lipei.tolist()

##che_chezhu = lipeibaodan[['车架号','车主']].drop_duplicates().apply(tuple,axis=1)
##che_toubao = lipeibaodan[['车架号','投保人']].drop_duplicates().apply(tuple,axis=1)
##che_jiashiyuan = lipeibaodan[['车架号','出险驾驶员证件号码']].drop_duplicates().apply(tuple,axis=1)
##che_lipei=lipeibaodan[['车架号','Claim ID']].drop_duplicates().apply(tuple,axis=1)

che_chezhu = lipeibaodan[['保单车牌','车主']].drop_duplicates().rename(columns={'车主':'Target','保单车牌':'Source'})
che_toubao = lipeibaodan[['保单车牌','投保人']].drop_duplicates().rename(columns={'投保人':'Target','保单车牌':'Source'})
che_jiashiyuan = lipeibaodan[['保单车牌','出险驾驶员证件号码']].drop_duplicates().rename(columns={'出险驾驶员证件号码':'Target','保单车牌':'Source'})
che_lipei=lipeibaodan[['保单车牌','Claim ID']].drop_duplicates().rename(columns={'Claim ID':'Target','保单车牌':'Source'})
sunshiche_lipei=lipeibaodan[['损失车辆号牌号码','Claim ID']].drop_duplicates().rename(columns={'Claim ID':'Target','损失车辆号牌号码':'Source'})

edges = pd.concat([che_chezhu,che_toubao,che_jiashiyuan,che_lipei,sunshiche_lipei]).drop_duplicates()
edges.to_csv('./out/edges/che_target.csv',sep=',',index=False)
time_start = time.time()
G=nx.from_pandas_edgelist(edges,'Source','Target')
time_end = time.time()
print('图填充完毕,用时:',time_end-time_start)
print('理赔数:' , len(lipei))
print('车数:' , len(che))
print('损失车数:', len(sunshiche))
print('车主:',len(chezhu))
print('投保人数:',len(toubaoren))
print('边数:',len(edges))
time_start = time.time()
partition = community.best_partition(G)
time_end = time.time()
print('louvain用时:',time_end-time_start)
parsize = len(set(partition.values()))
print('社区数',parsize)

plt.figure(figsize=(10.24,7.6))
edge_list = edges.values.tolist()

####开始全局画图
##node_color = []
##for n in G.nodes():
##    if n in che :
##        node_color.append('blue')
##    elif n in chezhu:
##        node_color.append('green')
##    elif n in toubaoren:
##        node_color.append('red')
##    elif n in jiashiyuan:
##        node_color.append('yellow')
##    elif n in lipei:
##        node_color.append('cyan')
##    else:
##        node_color.append('grey')
##
##time_start = time.time()
##nx.draw_spring(G,node_color= node_color,with_labels=True)
##time_end = time.time()
##print('画图用时:',time_end - time_start)
####plt.savefig('./out/partition.svg')
##plt.show()
procidx = 0
for com in set(partition.values()):
    
    com_nodes = [ nodes for nodes in partition.keys() if partition[nodes] == com]
    node_count = len(com_nodes)
    print('proc : ',procidx , '/',parsize,' node_count:',node_count,' id:',com)
    procidx = procidx+1
    dir_name = './out/partitions/' + str(node_count)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
##    if node_count < 8 :
##        print('\ttoo small passed')
##        
##        continue
##    if node_count > 100 :
##        print('\ttoo big passed')
##        continue
    elif node_count<=100:
        print('\t pass le 100')
        continue    
    time_start = time.time()
    local_ches = []
    local_chezhus =[]
    local_jiashiyuans = []
    local_lipeis =[]
    local_toubaorens = []
    local_sunshiches = []
    com_dirname = dir_name + "/" + str(com)
    if not os.path.exists(com_dirname):
        os.makedirs(com_dirname)
    edge_file = codecs.open(com_dirname+'/edges.csv','w+','utf-8')
    edge_writer = csv.writer(edge_file,delimiter=' ',quotechar=' ',quoting=csv.QUOTE_MINIMAL)
    che_file = codecs.open(com_dirname + '/che.csv','w+','utf-8')
    che_writer = csv.writer(che_file,delimiter=' ',quotechar=' ',quoting=csv.QUOTE_MINIMAL)
    sunshiche_file = codecs.open(com_dirname + '/sunshiche.csv','w+','utf-8')
    sunshiche_writer = csv.writer(sunshiche_file,delimiter=' ',quotechar=' ',quoting=csv.QUOTE_MINIMAL)
    chezhu_file = codecs.open(com_dirname + '/chezhu.csv','w+','utf-8')
    chezhu_writer = csv.writer(chezhu_file,delimiter=' ',quotechar=' ',quoting=csv.QUOTE_MINIMAL)
    toubaoren_file = codecs.open(com_dirname + '/toubaoren.csv','w+','utf-8')
    toubaoren_writer = csv.writer(toubaoren_file,delimiter=' ',quotechar=' ',quoting=csv.QUOTE_MINIMAL)
    jiashiyuan_file = codecs.open(com_dirname + '/jiashiyuan.csv','w+','utf-8')
    jiashiyuan_writer = csv.writer(jiashiyuan_file,delimiter=' ',quotechar=' ',quoting=csv.QUOTE_MINIMAL)
    lipei_file = codecs.open(com_dirname + '/lipei.csv','w+','utf-8')
    lipei_writer = csv.writer(lipei_file,delimiter=' ',quotechar=' ',quoting=csv.QUOTE_MINIMAL)
    time_end = time.time()
    print('\t准备用时:',time_end-time_start)
    time_start = time.time()
    for com_node in com_nodes:
        if com_node in che:
            local_ches.append(com_node)
        elif com_node in sunshiche:
            local_sunshiches.append(com_node)
        elif com_node in chezhu:
            local_chezhus.append(com_node)
        elif com_node in jiashiyuan:
            local_jiashiyuans.append(com_node)
        elif com_node in lipei:
            local_lipeis.append(com_node)
        elif com_node in toubaoren:
            local_toubaorens.append(com_node)
    local_relation = []
    time_end = time.time()
    print('\t节点计算用时:',time_end-time_start)

    
    time_start = time.time()
    for edge in edge_list:
        for lche in local_ches:
            for lchezhu in local_chezhus:
                if [lche,lchezhu] == edge:
                    local_relation.append([lche,lchezhu])
                    edge_writer.writerow([lche,lchezhu])
            for ljiashiyuan in local_jiashiyuans:
                if [lche,ljiashiyuan] == edge:
                    local_relation.append([lche,ljiashiyuan])
                    edge_writer.writerow([lche,ljiashiyuan])
            for ltoubaoren in local_toubaorens:
                if [ lche,ltoubaoren]==edge:
                    local_relation.append([lche,ltoubaoren])
                    edge_writer.writerow([lche,ltoubaoren])
            for llipei in local_lipeis:
                if [ lche,llipei] == edge:
                    local_relation.append([lche,llipei])
                    edge_writer.writerow([lche,llipei])
        for lsunshiche in local_sunshiches:
            for llipei in local_lipeis:
                if [lsunshiche,llipei] == edge:
                    local_relation.append([lsunshiche,llipei])
                    edge_writer.writerow([lsunshiche,llipei])
            
    time_end = time.time()
    print('\t边循环用时:',time_end-time_start)
    time_start = time.time()
    for lche in local_ches:
        che_writer.writerow([lche])
    for lchezhu in local_chezhus:
        chezhu_writer.writerow([lchezhu])
    for ljieashiyuan in local_jiashiyuans:
        jiashiyuan_writer.writerow([ljieashiyuan])
    for llipei in local_lipeis:
        lipei_writer.writerow([llipei])
    for ltoubaoren in local_toubaorens:
        toubaoren_writer.writerow([ltoubaoren])
    for lsunshiche in local_sunshiches:
        sunshiche_writer.writerow([lsunshiche])
    time_end = time.time()
    print('\t点循环用时:',time_end-time_start)
    time_start = time.time()
    G=nx.Graph()
    G.add_edges_from(local_relation)
        
    node_color = []
    for n in G.nodes():
        if n in local_ches :
            node_color.append('blue')
        elif n in local_chezhus:
            node_color.append('green')
        elif n in local_toubaorens:
            node_color.append('red')
        elif n in local_jiashiyuans:
            node_color.append('yellow')
        elif n in local_lipeis:
            node_color.append('cyan')
        else:
            node_color.append('grey')
    
    
    nx.draw_spring(G,node_color= node_color,with_labels=True)
    plt.savefig(com_dirname + '/figure.png')
##    plt.show()
    time_end = time.time()
    print('\t作图用时:',time_end-time_start)
    print('\t处理完:',com_dirname)
    plt.clf()



##    for lche in local_ches:
##        che_writer.writerow([lche])
##        for lchezhu in local_chezhus:
##            if [lche,lchezhu] in edge_list:
##                local_relation.append([lche,lchezhu])
##                edge_writer.writerow([lche,lchezhu])
##        for ljiashiyuan in local_jiashiyuans:
##            if [lche,ljiashiyuan]  in edge_list:
##                local_relation.append([lche,ljiashiyuan])
##                edge_writer.writerow([lche,ljiashiyuan])
##        for llipei in local_lipeis:
##            if [lche,llipei]  in edge_list:
##                local_relation.append([lche,llipei])
##                edge_writer.writerow([lche,llipei])
##        for ltoubaoren in local_toubaorens:
##            if [lche,ltoubaoren]  in edge_list:
##                local_relation.append([lche,ltoubaoren])
##                edge_writer.writerow([lche,ltoubaoren])
##    for lsunshiche in local_sunshiches:
##        for llipei in local_lipeis:
##            if [lsunshiche,llipei] in edge_list:
##                local_relation.append([lsunshiche,llipei])
##                edge_writer.writerow([lsunshiche,llipei])


