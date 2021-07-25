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
loopdir='thirddriverloops'
outdir='thirddriverout'

isExists = os.path.exists('./'+outdir+'/partitions')
if not isExists:
    os.makedirs('./'+outdir+'/partitions')

isExists = os.path.exists('./'+outdir+'/edges')
if not isExists:
    os.makedirs('./'+outdir+'/edges')

isExists = os.path.exists('./'+outdir+'/nodes')
if not isExists:
    os.makedirs('./'+outdir+'/nodes')

isExists = os.path.exists('./'+loopdir+'')
if not isExists:
    os.makedirs('./'+loopdir+'')

#####################
    
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
##
##juese.to_csv('./'+outdir+'/juese.csv',sep=',',header=['保单ID','投保人','被保人','车主'],index=False)
##
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
##baodan.to_csv('./'+outdir+'/baodan.csv',sep=',',header=['保单ID','车牌'],index=False)
##
##baodanjuese=pd.merge(baodan,juese,on=0,how='left')
####baodanjuese[0] = baodanjuese[0].str.split('.',expand=True)[0].str.strip()
##baodanjuese.columns =['保单ID','保单车牌','投保人','被保人','车主']
##baodanjuese.to_csv('./'+outdir+'/juesebaodan.csv',sep=',',index=False)
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
##lipei_ind.to_csv('./'+outdir+'/lipei_ind.csv',sep=',',index=False)
##lipei_dup.to_csv('./'+outdir+'/lipei_dup.csv',sep=',',index=False)
##
##
##chesun = pd.read_csv('./samples/chesun.csv',sep=',',header=None,encoding='gb18030',dtype={0:np.object})
##
##chesun.dropna(subset=[0,2,8],inplace=True)
##
##chesun = chesun[[0,2,8]]
##chesun = chesun[(chesun[2]!= 'a258e8d7a8f4a0e58ffef13d17281a83')]
##chesun = chesun[(chesun[8]!= 'cfcd208495d565ef66e7dff9f98764da')]
##
##chesun = chesun.drop_duplicates()
##
##chesun[0] = chesun[0].str.split('.',expand=True)[0].str.strip()
##chesun.columns=['Claim ID','损失车辆号牌号码','损失车辆驾驶员']
##chesun.to_csv('./'+outdir+'/chesun.csv',sep=',',index=False)
##
##
####lipei = pd.merge(lipei_ind,chesun,on='Claim ID',how='right')
####lipei.to_csv('./'+outdir+'/lipeichesun.csv',sep=',',index=False)
##
##lipeibaodan = pd.merge(lipei,baodanjuese,on='保单ID',how='left')
##lipeibaodan = lipeibaodan.drop_duplicates(subset=['Claim ID'])
##lipeibaodan = lipeibaodan[['Claim ID','保单ID','出险车辆号牌号码','保单车牌','投保人','被保人','车主','出险驾驶员证件号码']]
##haopaiwentishuju = lipeibaodan[(lipeibaodan['出险车辆号牌号码']!= lipeibaodan['保单车牌'])]
##
####lipeibaodan = lipeibaodan[(lipeibaodan['出险车辆号牌号码']== lipeibaodan['保单车牌'])]
##
##haopaiwentishuju.to_csv('./'+outdir+'/haopaiwentishuju.csv',sep=',',index=False)
##
##lipeibaodan.to_csv('./'+outdir+'/lipeibaodan.csv',sep=',',index=False)


#####################

lipeibaodan = pd.read_csv('./'+outdir+'/lipeibaodan.csv')
chesun = pd.read_csv('./' + outdir + '/chesun.csv')
#lipeibaodan = lipeibaodan.iloc[0:5000,:]
#chesun = chesun.iloc[0:5000,:]

che = lipeibaodan['保单车牌'].drop_duplicates()

chezhu=lipeibaodan['车主'].drop_duplicates()
chezhu.dropna(inplace=True)
toubaoren=lipeibaodan['投保人'].drop_duplicates()
toubaoren.dropna(inplace=True)
jiashiyuan=lipeibaodan['出险驾驶员证件号码'].drop_duplicates()
lipei=lipeibaodan['Claim ID'].drop_duplicates()
beibaoren=lipeibaodan['被保人'].drop_duplicates()
beibaoren.dropna(inplace=True)

sunshiche = chesun['损失车辆号牌号码'].drop_duplicates()
sunshichejiashiyuan = chesun['损失车辆驾驶员'].drop_duplicates()
sunshilipei= chesun['Claim ID'].drop_duplicates()
lipei=sunshilipei.append(lipei).drop_duplicates()


che.to_csv('./'+outdir+'/nodes/che.csv',sep=',',index=False)
chezhu.to_csv('./'+outdir+'/nodes/chezhu.csv',sep=',',index=False)
toubaoren.to_csv('./'+outdir+'/nodes/toubaoren.csv',sep=',',index=False)
jiashiyuan.to_csv('./'+outdir+'/nodes/jiashiyuan.csv',sep=',',index=False)
lipei.to_csv('./'+outdir+'/nodes/lipei.csv',sep=',',index=False)
sunshiche.to_csv('./'+outdir+'/nodes/sunshiche.csv',sep=',',index=False)
sunshichejiashiyuan.to_csv('./'+outdir+'/nodes/sunshichejiashiyuan.csv',sep=',',index=False)
beibaoren.to_csv('./'+outdir+'/nodes/beibaoren.csv',sep=',' ,index=False)


che = che.tolist()
chezhu=chezhu.tolist()
sunshiche = sunshiche.tolist()
toubaoren=toubaoren.tolist()
jiashiyuan=jiashiyuan.tolist()
lipei=lipei.tolist()
beibaoren=beibaoren.tolist()
sunshichejiashiyuan=sunshichejiashiyuan.tolist()

##che_chezhu = lipeibaodan[['车架号','车主']].drop_duplicates().apply(tuple,axis=1)
##che_toubao = lipeibaodan[['车架号','投保人']].drop_duplicates().apply(tuple,axis=1)
##che_jiashiyuan = lipeibaodan[['车架号','出险驾驶员证件号码']].drop_duplicates().apply(tuple,axis=1)
##che_lipei=lipeibaodan[['车架号','Claim ID']].drop_duplicates().apply(tuple,axis=1)

che_chezhu = lipeibaodan[['保单车牌','车主']].drop_duplicates().rename(columns={'车主':'Target','保单车牌':'Source'})
che_chezhu.dropna(subset=['Target'],inplace=True)
che_toubao = lipeibaodan[['保单车牌','投保人']].drop_duplicates().rename(columns={'投保人':'Target','保单车牌':'Source'})
che_toubao.dropna(subset=['Target'],inplace=True)
che_beibaoren = lipeibaodan[['保单车牌','被保人']].drop_duplicates().rename(columns={'被保人':'Target','保单车牌':'Source'})
che_beibaoren.dropna(subset=['Target'],inplace=True)
##che_jiashiyuan = lipeibaodan[['保单车牌','出险驾驶员证件号码']].drop_duplicates().rename(columns={'出险驾驶员证件号码':'Target','保单车牌':'Source'})
##jiashiyuan_lipei = lipeibaodan[['出险驾驶员证件号码','Claim ID']].drop_duplicates().rename(columns={'出险驾驶员证件号码':'Target','Claim ID':'Source'})
jiashiyuan_che = lipeibaodan[['出险驾驶员证件号码','出险车辆号牌号码']].drop_duplicates().rename(columns={'出险车辆号牌号码':'Source','出险驾驶员证件号码':'Target'})
che_lipei=lipeibaodan[['出险车辆号牌号码','Claim ID']].drop_duplicates().rename(columns={'Claim ID':'Source','出险车辆号牌号码':'Target'})

sunshiche_lipei=chesun[['损失车辆号牌号码','Claim ID']].drop_duplicates().rename(columns={'Claim ID':'Source','损失车辆号牌号码':'Target'})
sunshichejiashiyuan_che=chesun[['损失车辆驾驶员','损失车辆号牌号码']].drop_duplicates().rename(columns={'损失车辆号牌号码':'Source','损失车辆驾驶员':'Target'})

##edges = pd.concat([che_chezhu,che_toubao,ge,che_beibaoren,che_lipei,sunshiche_lipei,sunshiche_lipei,sunshichejiashiyuan_lipei]).drop_duplicates()
edges = pd.concat([che_chezhu,che_toubao,che_beibaoren,che_lipei,jiashiyuan_che,sunshiche_lipei,sunshichejiashiyuan_che]).drop_duplicates()
edges.to_csv('./'+outdir+'/edges.csv',sep=',',index=False)
time_start = time.time()
G=nx.from_pandas_edgelist(edges,'Source','Target')
time_end = time.time()
print('Fill Graph Finished Use Time:',time_end-time_start,'s')
print('Claim Count:' , len(lipei))
print('Car Count:' , len(che))
print('Car Owner:',len(chezhu))
print('Toubaoren Count:',len(toubaoren))
print('Beibaoren Count:', len(beibaoren))
print('Driver Count:',len(jiashiyuan))
print('Lost Car Count:', len(sunshiche))
print('LostCar Driver Count:',len(sunshichejiashiyuan))
print('Edge Count:',len(edges))
print('Node Count', len(G.nodes()))

time_start = time.time()
for n in G.nodes():
    node=G.nodes[n]
    node['fenlei']=set()
    node['chezhu']=''
    node['toubaoren']=''
    node['jiashiyuan']=set()
    node['lipei']=set()
    node['che']=set()
    node['sunshiche']=set()
    node['beibaoren']=set()
    
for idx,ccz in che_chezhu.iterrows():
    c=G.nodes[ccz['Source']]
    cz=G.nodes[ccz['Target']]
    c['fenlei'].add('che')
    c['chezhu']=ccz['Target']
    cz['fenlei'].add('chezhu')
    cz['che'].add(ccz['Source'])

for idx,ct in che_toubao.iterrows():
    c=G.nodes[ct['Source']]
    c['fenlei'].add('che')
    c['toubaoren']=ct['Target']
    t=G.nodes[ct['Target']]
    t['fenlei'].add('toubaoren')
    t['che'].add(ct['Source'])

for idx,cb in che_beibaoren.iterrows():
    c=G.nodes[cb['Source']]
    bbr=G.nodes[cb['Target']]
    c['fenlei'].add('che')
    c['beibaoren']=cb['Target']
    bbr['fenlei'].add('beibaoren')
    bbr['che'].add(cb['Source'])

# for idx,cj in che_jiashiyuan.iterrows():
#    c = G.nodes[cj['Source']]
#    c['fenlei'].add('che')
#    c['jiashiyuan'].add(cj['Target'])
#    j=G.nodes[cj['Target']]
#    j['fenlei'].add('jiashiyuan')
#    j['che'].add(cj['Source'])

for idx,cj in jiashiyuan_che.iterrows():
   c = G.nodes[cj['Source']]
   c['fenlei'].add('che')
   c['jiashiyuan'].add(cj['Target'])
   j=G.nodes[cj['Target']]
   j['fenlei'].add('jiashiyuan')
   j['che'].add(cj['Source'])

for idx,cl in che_lipei.iterrows():
    l=G.nodes[cl['Source']]
    c=G.nodes[cl['Target']]
    c['fenlei'].add('che')
    c['lipei'].add(cl['Source'])
    l['fenlei'].add('lipei')
    l['che'].add(cl['Target'])

for idx,sl in sunshiche_lipei.iterrows():
    l=G.nodes[sl['Source']]
    s=G.nodes[sl['Target']]
    s['fenlei'].add('sunshiche')
    s['lipei'].add(sl['Source'])
    l['fenlei'].add('lipei')
    l['sunshiche'].add(sl['Target'])

##for idx,jl in jiashiyuan_lipei.iterrows():
##    l=G.nodes[jl['Source']]
##    l['fenlei'].add('lipei')
##    l['jiashiyuan'].add(jl['Target'])
##    j=G.nodes[jl['Target']]
##    j['fenlei'].add('jiashiyuan')
##    j['lipei'].add(jl['Source'])

for idx,sjl in sunshichejiashiyuan_che.iterrows():
    l=G.nodes[sjl['Source']]
    l['fenlei'].add('sunshiche')
    l['jiashiyuan'].add(sjl['Target'])
    j=G.nodes[sjl['Target']]
    j['fenlei'].add('jiashiyuan')
    j['sunshiche'].add(sjl['Source'])


time_end = time.time()
print('Fill Porperties Time:',time_end - time_start,'s')


time_start = time.time()
partition = community.best_partition(G)
time_end = time.time()
print('Find Partition Time:',time_end-time_start)
parsize = len(set(partition.values()))
print('Community Count:',parsize)

##plt.figure(figsize=(10.24,7.6))
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
####plt.savefig('./'+outdir+'/partition.svg')
##plt.show()
procidx = 0
for com in set(partition.values()):
    
    com_nodes = [ nodes for nodes in partition.keys() if partition[nodes] == com]
    node_count = len(com_nodes)
    
    print('proc : ',procidx , '/',parsize,' node_count:',node_count,' id:',com)
    procidx = procidx+1
    if node_count < 7 :
        print('\ttoo small passed')
        continue

    if node_count > 300 :
        print('\ttoo big passed')
        continue
##    if node_count<=100:
##        print('\t pass le 100')
##        continue   
    dir_name = './'+outdir+'/partitions/' + str(node_count)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
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
    beibaoren_file = codecs.open(com_dirname + '/beibaoren.csv','w+','utf-8')
    beibaoren_writer = csv.writer(beibaoren_file,delimiter=' ',quotechar=' ',quoting=csv.QUOTE_MINIMAL)
    time_end = time.time()
    print('\tPrepare Node Files Time:',time_end-time_start)
    time_start = time.time()
        
    lG=nx.Graph()
    for com_node in com_nodes:
        
        node = G.nodes[com_node]
        lG.add_node(com_node)
        
        for fenlei in iter(node['fenlei']):
            if fenlei == 'sunshiche':
                sunshiche_writer.writerow([com_node])
                if node['chezhu']:
                    lG.add_node(node['chezhu'])
                    lG.add_edge(com_node,node['chezhu'])

                if node['toubaoren']:
                    lG.add_node(node['toubaoren'])
                    lG.add_edge(com_node,node['toubaoren'])

                if node['beibaoren']:
                    lG.add_node(node['beibaoren'])
                    lG.add_edge(com_node,node['beibaoren'])

                if len(node['lipei'])>0:
                    lG.add_nodes_from(list(node['lipei']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['lipei'])])

                if len(node['jiashiyuan'])>0:
                    lG.add_nodes_from(list(node['jiashiyuan']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['jiashiyuan'])])
            elif fenlei == 'che':
                che_writer.writerow([com_node])
                if node['chezhu']:
                    lG.add_node(node['chezhu'])
                    lG.add_edge(com_node,node['chezhu'])

                if node['toubaoren']:
                    lG.add_node(node['toubaoren'])
                    lG.add_edge(com_node,node['toubaoren'])

                if node['beibaoren']:
                    lG.add_node(node['beibaoren'])
                    lG.add_edge(com_node,node['beibaoren'])

                if len(node['lipei'])>0:
                    lG.add_nodes_from(list(node['lipei']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['lipei'])])

                if len(node['jiashiyuan'])>0:
                    lG.add_nodes_from(list(node['jiashiyuan']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['jiashiyuan'])])
                    
            elif fenlei == 'toubaoren':
                toubaoren_writer.writerow([com_node])
                if len(node['che'])>0:
                    lG.add_nodes_from(list(node['che']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['che'])])

            elif fenlei=='jiashiyuan':
                jiashiyuan_writer.writerow([com_node])
                if len(node['lipei'])>0:
                    lG.add_nodes_from(list(node['lipei']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['lipei'])])
                if len(node['che'])>0:
                    lG.add_nodes_from(list(node['che']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['che'])])
                    
            elif fenlei=='beibaoren':
                beibaoren_writer.writerow([com_node])
                if len(node['che'])>0:
                    lG.add_nodes_from(list(node['che']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['che'])])
                    
            elif fenlei == 'chezhu' :
                chezhu_writer.writerow([com_node])
                if len(node['che'])>0:
                    lG.add_nodes_from(list(node['che']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['che'])])
                
            elif fenlei == 'sunchiche':
                sunshiche_writer.writerow([com_node])
                if len(node['jiashiyuan'])>0:
                    lG.add_nodes_from(list(node['jiashiyuan']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['jiashiyuan'])])
                if len(node['lipei'])>0:
                    lG.add_nodes_from(list(node['lipei']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['lipei'])])

            elif fenlei == 'lipei':
                lipei_writer.writerow([com_node])
                if len(node['che'])>0:
                    lG.add_nodes_from(list(node['che']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['che'])])

                if len(node['sunshiche'])>0:
                    lG.add_nodes_from(list(node['sunshiche']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['sunshiche'])])

                if len(node['jiashiyuan'])>0:
                    lG.add_nodes_from(list(node['jiashiyuan']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['jiashiyuan'])])


    Gnode_color = []
    for lnode in lG.nodes():
        n = G.nodes[lnode]
        if 'che' in n['fenlei'] :
            Gnode_color.append('blue')
        elif 'chezhu' in n['fenlei'] :
            Gnode_color.append('green')
        elif 'toubaoren' in n['fenlei'] :
            Gnode_color.append('red')
        elif 'beibaoren' in n['fenlei']:
            Gnode_color.append('purple')
        elif 'jiashiyuan' in n['fenlei'] :
            Gnode_color.append('yellow')
        elif 'lipei' in n['fenlei'] :
            Gnode_color.append('cyan')
        elif 'sunshiche' in n['fenlei']:
            Gnode_color.append('black')
        else:
            Gnode_color.append('grey')

    
    for egs in lG.edges():
        edge_writer.writerow(list(egs))

    hasLoop = False
    try:
        f1 = nx.algorithms.find_cycle(lG)
        if f1:
            hasLoop = True
    except:
        pass
    nx.draw_spring(lG,node_color=Gnode_color,with_labels=True)
    ##plt.show()
    plt.savefig(com_dirname + '/figure.png')
    if hasLoop:
        plt.savefig('./'+loopdir+'/' + str(node_count) + '_' + str(com) + '.png')
    plt.clf()
    nx.draw_spring(lG,node_color=Gnode_color)
    plt.savefig(com_dirname + '/figure_nolabel.png')
    if hasLoop:
        plt.savefig('./'+loopdir+'/' + str(node_count) + '_' + str(com) + 'nolabel.png')
    plt.clf()

    

    





