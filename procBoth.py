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

print(os.getcwd())
indir=r'两家一起/摘取出数据/华安'
outdir=r'两家一起/计算结果'
loopdir=outdir + '/loops'
badloopdir = outdir + '/badloops'
suslipeidir = outdir + '/suslipei'

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

isExists = os.path.exists('./'+badloopdir+'')
if not isExists:
    os.makedirs('./'+badloopdir+'')

isExists = os.path.exists('./'+suslipeidir+'')
if not isExists:
    os.makedirs('./'+suslipeidir+'')

isExists = os.path.exists('./两家一起/tmplog')
if not isExists:
    os.makedirs('./两家一起/tmplog')


#华安
juese = pd.read_csv(indir + r'/保单角色信息表.csv',encoding='utf8',dtype={0:np.object})
baodan = pd.read_csv(indir+r'/保单信息表.csv',encoding='utf8',dtype={0:np.object,1:np.object})
chesun = pd.read_csv(indir+r'/车损信息.csv',encoding='utf8',dtype={0:np.object,3:np.object,5:np.object,8:np.object})
shangzhe = pd.read_csv(indir + r'/人伤信息.csv',encoding='utf8',dtype={0:np.object})
    
lipeiinfo = pd.read_csv(indir+'/理赔信息表.csv',encoding='utf8',dtype={0:np.object,6:np.object,7:np.object,12:np.object,14:np.object,15:np.object})
peifuinfo = pd.read_csv(indir+'/赔付信息表.csv',encoding='utf8',dtype={0:np.object})

wentilipei = lipeiinfo[(lipeiinfo[r'案件状态']==r'零结')&(lipeiinfo[r'赔付金额']!=0)]
wentilipei.to_csv(r'./两家一起/tmplog/问题理赔.csv',sep=',',index=False)

zhengchanglipei = lipeiinfo[(lipeiinfo[r'案件状态']==r'正常')]
zhengchanglipei.to_csv(r'./两家一起/tmplog/正常理赔.csv',sep=',',index=False)

print(r'问题理赔数量', len(wentilipei))
print(r'问题理赔的赔付金额总数',wentilipei[[r'赔付金额']].sum()[0])
print(r'正常理赔数量', len(zhengchanglipei))
print(r'正常理赔的赔付金额总数',zhengchanglipei[[r'赔付金额']].sum()[0])

tmpf = open('./两家一起/tmplog/runLog.txt','w')
tmpf.write(r'问题理赔的赔付金额总数:'+str(wentilipei[[r'赔付金额']].sum()[0]) + '\n');
tmpf.write(r'问题理赔数量:'+str(len(wentilipei))+ '\n')
tmpf.write(r'正常理赔的赔付金额总数:'+str(zhengchanglipei[[r'赔付金额']].sum()[0]) + '\n');
tmpf.write(r'正常理赔数量:'+str(len(zhengchanglipei))+ '\n')

baodan_che = baodan[[r'保单ID',r'理赔ID',r'车架号']]
juese_baodan = juese[[r'保单ID',r'车主证件号',r'投保人证件号',r'被保险人证件号']]

juese_che = pd.merge(baodan_che,juese_baodan,on=r'保单ID',how='inner')

chezhu_che = juese_che[[r'车架号',r'车主证件号']]
toubao_che = juese_che[[r'车架号',r'投保人证件号']]
beibao_che = juese_che[[r'车架号',r'被保险人证件号']]

lipei_shangzhe = shangzhe[[r'理赔ID',r'伤者证件号']]

shigu_che = chesun[[r'理赔ID',r'车架号']]

che = baodan[r'车架号'].append(chesun[r'车架号']).drop_duplicates()
jiashiyuan = chesun[r'出险驾驶员证件号码'].drop_duplicates()
lipei=chesun[r'理赔ID'].drop_duplicates()
toubao = juese[r'投保人证件号'].drop_duplicates()
chezhu = juese[r'车主证件号'].drop_duplicates()
beibao = juese[r'被保险人证件号'].drop_duplicates()
shangzhe = lipei_shangzhe[r'伤者证件号'].drop_duplicates()

che.to_csv('./'+outdir+'/nodes/che.csv',encoding='utf-8-sig',sep=',',index=False)
chezhu.to_csv('./'+outdir+'/nodes/chezhu.csv',encoding='utf-8-sig',sep=',',index=False)
toubao.to_csv('./'+outdir+'/nodes/toubao.csv',encoding='utf-8-sig',sep=',',index=False)
jiashiyuan.to_csv('./'+outdir+'/nodes/jiashiyuan.csv',encoding='utf-8-sig',sep=',',index=False)
lipei.to_csv('./'+outdir+'/nodes/lipei.csv',encoding='utf-8-sig',sep=',',index=False)
beibao.to_csv('./'+outdir+'/nodes/beibao.csv',encoding='utf-8-sig',sep=',' ,index=False)
shangzhe.to_csv('./'+outdir+'/nodes/shangzhe.csv',encoding='utf-8-sig',sep=',',index=False)

che = che.tolist()
chezhu=chezhu.tolist()
toubao=toubao.tolist()
jiashiyuan=jiashiyuan.tolist()
lipei=lipei.tolist()
beibao=beibao.tolist()
shangzhe=shangzhe.tolist()

che_chezhu = juese_che[['车架号','车主证件号']].drop_duplicates().rename(columns={'车主证件号':'Target','车架号':'Source'})
che_toubao = juese_che[['车架号','投保人证件号']].drop_duplicates().rename(columns={'投保人证件号':'Target','车架号':'Source'})
che_beibao = juese_che[['车架号','被保险人证件号']].drop_duplicates().rename(columns={'被保险人证件号':'Target','车架号':'Source'})
che_jiashiyuan = chesun[['车架号','出险驾驶员证件号码']].drop_duplicates().dropna().rename(columns={'出险驾驶员证件号码':'Target','车架号':'Source'})
che_lipei=chesun[['车架号','理赔ID']].drop_duplicates().rename(columns={'理赔ID':'Target','车架号':'Source'})
lipei_shangzhe = lipei_shangzhe.rename(columns={r'理赔ID':'Target',r'伤者证件号':'Source'})

##加载中保信
indir=r'./两家一起/摘取出数据/中保信'
zbxlipeibaodan = pd.read_csv(indir+'/lipeibaodan.csv',encoding='utf8',dtype={0:np.dtype(str)})
zbxchesun = pd.read_csv(indir + '/chesun.csv',encoding='utf8',dtype={0:np.dtype(str)})
zbxche = zbxlipeibaodan[r'车架号'].drop_duplicates()

zbxchezhu=zbxlipeibaodan[r'车主'].drop_duplicates()
zbxchezhu.dropna(inplace=True)
zbxtoubaoren=zbxlipeibaodan[r'投保人'].drop_duplicates()
zbxtoubaoren.dropna(inplace=True)
zbxjiashiyuan=zbxlipeibaodan[r'出险驾驶员证件号码'].drop_duplicates()
zbxlipei=zbxlipeibaodan['Claim ID'].drop_duplicates()
zbxbeibaoren=zbxlipeibaodan[r'被保人'].drop_duplicates()
zbxbeibaoren.dropna(inplace=True)

zbxsunshiche = zbxchesun[r'车架号'].drop_duplicates()
zbxsunshichejiashiyuan = zbxchesun[r'损失车辆驾驶员'].drop_duplicates()
zbxsunshilipei= zbxchesun['Claim ID'].drop_duplicates()
zbxlipei=zbxsunshilipei.append(zbxlipei).drop_duplicates()


zbxche.to_csv(outdir+'/nodes/zbxche.csv',sep=',',index=False)
zbxchezhu.to_csv(outdir+'/nodes/zbxchezhu.csv',sep=',',index=False)
zbxtoubaoren.to_csv(outdir+'/nodes/zbxtoubaoren.csv',sep=',',index=False)
zbxjiashiyuan.to_csv(outdir+'/nodes/zbxjiashiyuan.csv',sep=',',index=False)
zbxlipei.to_csv(outdir+'/nodes/zbxlipei.csv',sep=',',index=False)
zbxsunshiche.to_csv(outdir+'/nodes/zbxsunshiche.csv',sep=',',index=False)
zbxsunshichejiashiyuan.to_csv(outdir+'/nodes/zbxsunshichejiashiyuan.csv',sep=',',index=False)
zbxbeibaoren.to_csv(outdir+'/nodes/zbxbeibaoren.csv',sep=',' ,index=False)
zbxche = zbxche.tolist()
zbxchezhu=zbxchezhu.tolist()
zbxsunshiche = zbxsunshiche.tolist()
zbxtoubaoren=zbxtoubaoren.tolist()
zbxjiashiyuan=zbxjiashiyuan.tolist()
zbxlipei=zbxlipei.tolist()
zbxbeibaoren=zbxbeibaoren.tolist()
zbxsunshichejiashiyuan=zbxsunshichejiashiyuan.tolist()
zbxche_chezhu = zbxlipeibaodan[[r'车架号',r'车主']].drop_duplicates().rename(columns={r'车主':'Target',r'车架号':'Source'})
zbxche_toubao = zbxlipeibaodan[[r'车架号',r'投保人']].drop_duplicates().rename(columns={r'投保人':'Target',r'车架号':'Source'})
zbxche_chezhu.dropna(subset=['Target','Source'],inplace=True)
zbxche_toubao.dropna(subset=['Target','Source'],inplace=True)
zbxche_beibaoren = zbxlipeibaodan[[r'车架号',r'被保人']].drop_duplicates().rename(columns={r'被保人':'Target',r'车架号':'Source'})
zbxche_beibaoren.dropna(subset=['Target','Source'],inplace=True)
zbxjiashiyuan_lipei = zbxlipeibaodan[[r'出险驾驶员证件号码','Claim ID']].drop_duplicates().rename(columns={r'出险驾驶员证件号码':'Target','Claim ID':'Source'})

zbxche_lipei=zbxlipeibaodan[[r'车架号','Claim ID']].drop_duplicates().rename(columns={'Claim ID':'Source',r'车架号':'Target'})
zbxsunshiche_lipei=zbxchesun[[r'车架号','Claim ID']].drop_duplicates().rename(columns={'Claim ID':'Source',r'车架号':'Target'})
zbxsunshichejiashiyuan_lipei=zbxchesun[[r'损失车辆驾驶员','Claim ID']].drop_duplicates().rename(columns={'Claim ID':'Source',r'损失车辆驾驶员':'Target'})

edges = pd.concat([
                   che_chezhu,che_toubao,che_jiashiyuan,che_beibao,che_lipei,lipei_shangzhe,
                   zbxche_chezhu,zbxche_toubao,zbxche_beibaoren,zbxche_lipei,
                   #zbxjiashiyuan_lipei,
                   zbxsunshiche_lipei,
                   #zbxsunshichejiashiyuan_lipei
                   ]
                  ).drop_duplicates()
edges.to_csv(outdir+'/edges.csv',sep=',',index=False)

time_start = time.time()
G=nx.from_pandas_edgelist(edges,'Source','Target')
time_end = time.time()


#图中华安
for n in G.nodes():
    node=G.nodes[n]
    node['fenlei']=set()
    node['chezhu']=''
    node['toubao']=''
    node['jiashiyuan']=set()
    node['lipei']=set()
    node['che']=set()
    node['beibao']=set()
    node['shangzhe']=set()
    node['sunshiche']=set()
    node['laiyuan']=r'华安'

for idx,ccz in zbxche_chezhu.iterrows():
    c=G.nodes[ccz['Source']]
    c['laiyuan']=r'中保信'
    cz=G.nodes[ccz['Target']]
    cz['laiyuan']=r'中保信'
    c['fenlei'].add('che')
    c['chezhu']=ccz['Target']
    cz['fenlei'].add('chezhu')
    cz['che'].add(ccz['Source'])

for idx,ct in zbxche_toubao.iterrows():
    c=G.nodes[ct['Source']]
    c['laiyuan']=r'中保信'
    c['fenlei'].add('che')
    c['toubao']=ct['Target']
    t=G.nodes[ct['Target']]
    t['laiyuan']=r'中保信'
    t['fenlei'].add('toubao')
    t['che'].add(ct['Source'])

for idx,cb in zbxche_beibaoren.iterrows():
    c=G.nodes[cb['Source']]
    c['laiyuan']=r'中保信'
    bbr=G.nodes[cb['Target']]
    c['fenlei'].add('che')
    c['beibao']=cb['Target']
    bbr['fenlei'].add('beibao')
    bbr['che'].add(cb['Source'])

for idx,cl in zbxche_lipei.iterrows():
    l=G.nodes[cl['Source']]
    l['laiyuan']=r'中保信'
    c=G.nodes[cl['Target']]
    c['laiyuan']=r'中保信'
    c['fenlei'].add('che')
    c['lipei'].add(cl['Source'])
    l['fenlei'].add('lipei')
    l['che'].add(cl['Target'])

for idx,sl in zbxsunshiche_lipei.iterrows():
    l=G.nodes[sl['Source']]
    l['laiyuan']=r'中保信'
    s=G.nodes[sl['Target']]
    s['laiyuan']=r'中保信'
    s['fenlei'].add('sunshiche')
    s['lipei'].add(sl['Source'])
    l['fenlei'].add('lipei')
    l['sunshiche'].add(sl['Target'])

#for idx,jl in zbxjiashiyuan_lipei.iterrows():
#    l=G.nodes[jl['Source']]
#    l['laiyuan']=r'中保信'
#    l['fenlei'].add('lipei')
#    l['jiashiyuan'].add(jl['Target'])
#    j=G.nodes[jl['Target']]
#    j['laiyuan']=r'中保信'
#    j['fenlei'].add('jiashiyuan')
#    j['lipei'].add(jl['Source'])

#for idx,sjl in zbxsunshichejiashiyuan_lipei.iterrows():
#    l=G.nodes[sjl['Source']]
#    l['laiyuan']=r'中保信'
#    l['fenlei'].add('lipei')
#    l['jiashiyuan'].add(sjl['Target'])
#    j=G.nodes[sjl['Target']]
#    j['laiyuan']=r'中保信'
#    j['fenlei'].add('jiashiyuan')
#    j['lipei'].add(sjl['Source'])
    
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
    c['toubao']=ct['Target']
    t=G.nodes[ct['Target']]
    t['fenlei'].add('toubao')
    t['che'].add(ct['Source'])

for idx,cb in che_beibao.iterrows():
    c=G.nodes[cb['Source']]
    bbr=G.nodes[cb['Target']]
    c['fenlei'].add('che')
    c['beibao']=cb['Target']
    bbr['fenlei'].add('beibao')
    bbr['che'].add(cb['Source'])

for idx,cj in che_jiashiyuan.iterrows():
    c = G.nodes[cj['Source']]
    c['fenlei'].add('che')
    c['jiashiyuan'].add(cj['Target'])
    j=G.nodes[cj['Target']]
    j['fenlei'].add('jiashiyuan')
    j['che'].add(cj['Source'])

for idx,cl in che_lipei.iterrows():
    c=G.nodes[cl['Source']]
    c['fenlei'].add('che')
    c['lipei'].add(cl['Target'])
    l=G.nodes[cl['Target']]
    l['fenlei'].add('lipei')
    l['che'].add(cl['Source'])

for idx,sz in lipei_shangzhe.iterrows():
    c=G.nodes[sz['Source']]
    c['fenlei'].add('shangzhe')
    c['lipei'].add(sz['Target'])
    l=G.nodes[sz['Target']]
    l['fenlei'].add('lipei')
    l['shangzhe'].add(sz['Source'])

partition = community.best_partition(G)
parsize = len(set(partition.values()))
procidx = 0
for com in set(partition.values()):
    
    com_nodes = [ nodes for nodes in partition.keys() if partition[nodes] == com]
    node_count = len(com_nodes)
    print('proc : ',procidx , '/',parsize,' node_count:',node_count,' id:',com)
    procidx = procidx+1
    dir_name = './'+outdir+'/partitions/' + str(node_count)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    local_ches = []
    local_chezhus =[]
    local_jiashiyuans = []
    local_lipeis =[]
    local_toubaos = []
    local_shangzhes = []
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
    toubao_file = codecs.open(com_dirname + '/toubao.csv','w+','utf-8')
    toubao_writer = csv.writer(toubao_file,delimiter=' ',quotechar=' ',quoting=csv.QUOTE_MINIMAL)
    jiashiyuan_file = codecs.open(com_dirname + '/jiashiyuan.csv','w+','utf-8')
    jiashiyuan_writer = csv.writer(jiashiyuan_file,delimiter=' ',quotechar=' ',quoting=csv.QUOTE_MINIMAL)
    lipei_file = codecs.open(com_dirname + '/lipei.csv','w+','utf-8')
    lipei_writer = csv.writer(lipei_file,delimiter=' ',quotechar=' ',quoting=csv.QUOTE_MINIMAL)
    beibao_file = codecs.open(com_dirname + '/beibao.csv','w+','utf-8')
    beibao_writer = csv.writer(beibao_file,delimiter=' ',quotechar=' ',quoting=csv.QUOTE_MINIMAL)
    shangzhe_file = codecs.open(com_dirname + '/shangzhe.csv','w+','utf-8')
    shangzhe_writer = csv.writer(shangzhe_file,delimiter=' ',quotechar=' ',quoting=csv.QUOTE_MINIMAL)

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

                if node['toubao']:
                    lG.add_node(node['toubao'])
                    lG.add_edge(com_node,node['toubao'])

                if len(node['jiashiyuan'])>0:
                    lG.add_nodes_from(list(node['jiashiyuan']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['jiashiyuan'])])

                if len(node['beibao'])>0:
                    lG.add_node(node['beibao'])
                    lG.add_edge(com_node,node['beibao'])

                if len(node['lipei'])>0:
                    lG.add_nodes_from(list(node['lipei']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['lipei'])])
            elif fenlei == 'che':
                che_writer.writerow([com_node])
                if node['chezhu']:
                    lG.add_node(node['chezhu'])
                    lG.add_edge(com_node,node['chezhu'])

                if node['toubao']:
                    lG.add_node(node['toubao'])
                    lG.add_edge(com_node,node['toubao'])

                if len(node['beibao'])>0:
                    lG.add_node(node['beibao'])
                    lG.add_edge(com_node,node['beibao'])

                if len(node['jiashiyuan'])>0:
                    lG.add_nodes_from(list(node['jiashiyuan']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['jiashiyuan'])])

                if len(node['lipei'])>0:
                    lG.add_nodes_from(list(node['lipei']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['lipei'])])
            if fenlei == 'sunshiche':
                sunshiche_writer.writerow([com_node])
                if node['chezhu']:
                    lG.add_node(node['chezhu'])
                    lG.add_edge(com_node,node['chezhu'])

                if node['toubao']:
                    lG.add_node(node['toubao'])
                    lG.add_edge(com_node,node['toubao'])

                if node['beibao']:
                    lG.add_node(node['beibao'])
                    lG.add_edge(com_node,node['beibao'])

                if len(node['jiashiyuan'])>0:
                    lG.add_nodes_from(list(node['jiashiyuan']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['jiashiyuan'])])

                if len(node['lipei'])>0:
                    lG.add_nodes_from(list(node['lipei']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['lipei'])])
            elif fenlei == 'toubao':
                toubao_writer.writerow([com_node])
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
                    
            elif fenlei=='beibao':
                beibao_writer.writerow([com_node])
                if len(node['che'])>0:
                    lG.add_nodes_from(list(node['che']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['che'])])
                    
            elif fenlei == 'chezhu' :
                chezhu_writer.writerow([com_node])
                if len(node['che'])>0:
                    lG.add_nodes_from(list(node['che']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['che'])])
                    
            elif fenlei == 'shangzhe' :
                shangzhe_writer.writerow([com_node])
                if len(node['lipei'])>0:
                    lG.add_nodes_from(list(node['lipei']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['lipei'])])
                    
            elif fenlei == 'lipei':
                lipei_writer.writerow([com_node])
                local_lipeis.append(com_node)
                if len(node['che'])>0:
                    lG.add_nodes_from(list(node['che']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['che'])])
                if len(node['sunshiche'])>0:
                    lG.add_nodes_from(list(node['sunshiche']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['sunshiche'])])
                if len(node['shangzhe'])>0:
                    lG.add_nodes_from(list(node['shangzhe']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['shangzhe'])])


    Gnode_color = []
    for lnode in lG.nodes():
        n = G.nodes[lnode]
        if 'che' in n['fenlei'] :
            if n['laiyuan']==r'中保信':
                Gnode_color.append('darkblue')
            else:
                Gnode_color.append('blue')
        elif 'shangzhe' in n['fenlei']:
            Gnode_color.append('brown')
        elif 'chezhu' in n['fenlei'] :
            Gnode_color.append('orange')
        elif 'jiashiyuan' in n['fenlei'] :
            Gnode_color.append('yellow')
        elif 'toubao' in n['fenlei'] :
            Gnode_color.append('red')
        elif 'beibao' in n['fenlei']:
            Gnode_color.append('purple')
        elif 'lipei' in n['fenlei'] :
            if n['laiyuan']==r'中保信':
                Gnode_color.append('seagreen')
            else:
                Gnode_color.append('green')
        elif 'sunshiche' in n['fenlei']:
            Gnode_color.append('black')
        else:
            print('not support fenlei:',n['fenlei'])
            Gnode_color.append('gray')

    
    for egs in lG.edges():
        edge_writer.writerow(list(egs))

    lipeinodes='|'.join(local_lipeis)
    locallipeiinfo = lipeiinfo[(lipeiinfo[r'理赔ID'].str.contains(lipeinodes))]
    locallipeiinfo.to_csv(com_dirname + r'/华安理赔信息表.csv',sep=',',index=False)

    localbaodanxinxi = baodan[(baodan[r'理赔ID'].str.contains(lipeinodes))]

    if len(localbaodanxinxi) > 0:
        
        localbaodanxinxi.to_csv(com_dirname + r'/华安保单信息表.csv', sep = ',', index=False)
        localbaodanids = localbaodanxinxi[[r'保单ID']].drop_duplicates()[r'保单ID'].tolist()
        localbandanidsstr = '|'.join(localbaodanids)
    
        localjueseinfo = juese[(juese[r'保单ID'].str.contains(localbandanidsstr))]
        localjueseinfo.to_csv(com_dirname + r'/华安保单角色信息表.csv',sep=',',index=False)

    localchesuninfo = chesun[(chesun[r'理赔ID'].str.contains(lipeinodes))]
    localchesuninfo.to_csv(com_dirname + r'/华安车损信息.csv',sep=',',index=False)

    localpeifu = peifuinfo[(peifuinfo[r'理赔ID'].str.contains(lipeinodes))]
    localpeifu.to_csv(com_dirname + r'/华安赔付信息表.csv',sep=',',index=False)

    localzbxlipeibaodan = zbxlipeibaodan[(zbxlipeibaodan[r'Claim ID'].str.contains(lipeinodes))]
    localzbxlipeibaodan.to_csv(com_dirname + r'/中保信理赔保单信息.csv',sep=',',index=False)
    
    
    localzbxchesun = zbxchesun[(zbxchesun[r'Claim ID'].str.contains(lipeinodes))]
    localzbxchesun.to_csv(com_dirname + r'/中保信车损.csv',sep=',',index=False)
    
    hasLoop = False
    try:
        f1 = nx.algorithms.cycle_basis(lG)
        if f1:
            hasLoop = True
    except Exception as e:
        print("！！！！！！！！！！！Get Except ",e)
        pass

    
    print("hasLoop",hasLoop)
    nx.draw_spring(lG,node_color=Gnode_color,with_labels=True,node_size=128)
    
    plt.savefig(com_dirname + '/figure.png')
    if hasLoop:
        plt.savefig('./'+loopdir+'/' + str(node_count) + '_' + str(com) + '.png')
    
    plt.clf()
    nx.draw_spring(lG,node_color=Gnode_color,node_size=182)
    plt.savefig(com_dirname + '/figure_nolabel.png')

    if hasLoop:
        plt.savefig('./'+loopdir+'/' + str(node_count) + '_' + str(com) + 'no_label.png')
    
    plt.clf()
            
plt.clf()

#nx.draw_spring(G,with_labels=False,node_shape='v')
#plt.show()
