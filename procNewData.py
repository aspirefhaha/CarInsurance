# -*-encoding:utf-8 -*-
#/usr/bin/python3

import pandas as pd
import numpy as np
import community
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import scipy
import time
import datetime
import os
import csv
import codecs

print(os.getcwd())
outdir='fraud_data0602'
loopdir=outdir + '/loops'
badloopdir = outdir + '/badloops'

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

isExists = os.path.exists('./tmpout')
if not isExists:
    os.makedirs('./tmpout')
    
samplenum=0

if samplenum != 0:
    juese = pd.read_csv(outdir + r'/juese.csv',encoding='utf8',dtype={0:np.object},nrows=samplenum)
    baodan = pd.read_csv(outdir+r'/baodanxinxi.csv',encoding='utf8',dtype={0:np.object,1:np.object},nrows=samplenum)
    chesun = pd.read_csv(outdir+r'/chesun.csv',encoding='utf8',dtype={0:np.object},nrows=samplenum)
    shangzheinfo = pd.read_csv(outdir + r'/renshang.csv',encoding='utf8',dtype={0:np.object},nrows=samplenum)
else:
    juese = pd.read_csv(outdir + r'/juese.csv',encoding='utf8',dtype={0:np.object})
    baodan = pd.read_csv(outdir+r'/baodanxinxi.csv',encoding='utf8',dtype={0:np.object,1:np.object})
    chesun = pd.read_csv(outdir+r'/chesun.csv',encoding='utf8',dtype={0:np.object})
    shangzheinfo = pd.read_csv(outdir + r'/renshang.csv',encoding='utf8',dtype={0:np.object})
    
lipeiinfo = pd.read_csv(outdir+'/lipei.csv',encoding='utf8',dtype={0:np.object})
peifuinfo = pd.read_csv(outdir+'/peifu.csv',encoding='utf8',dtype={0:np.object})

wentilipei = lipeiinfo[(lipeiinfo[r'????????????']==r'??????')&(lipeiinfo[r'????????????']!=0)]
wentilipei.to_csv('./tmpout/wentilipei.csv',sep=',',index=False)

zhengchanglipei = lipeiinfo[(lipeiinfo[r'????????????']==r'??????')]
zhengchanglipei.to_csv('./tmpout/zhengchanglipei.csv',sep=',',index=False)



print(r'??????????????????', len(wentilipei))
print(r'?????????????????????????????????',wentilipei[[r'????????????']].sum()[0])
print(r'??????????????????', len(zhengchanglipei))
print(r'?????????????????????????????????',zhengchanglipei[[r'????????????']].sum()[0])

tmpf = open('./tmpout/runLog.txt','w')
tmpf.write(r'?????????????????????????????????:'+str(wentilipei[[r'????????????']].sum()[0]) + '\n');
tmpf.write(r'??????????????????:'+str(len(wentilipei))+ '\n')
tmpf.write(r'?????????????????????????????????:'+str(zhengchanglipei[[r'????????????']].sum()[0]) + '\n');
tmpf.write(r'??????????????????:'+str(len(zhengchanglipei))+ '\n')


##baodan_groupd = baodan.groupby(r'??????ID')
##baodan_groupd.count().to_csv(r'baodan??????.csv',encoding='utf-8-sig',mode='w+')

baodan_che = baodan[[r'??????ID',r'??????ID',r'?????????']]
juese_baodan = juese[[r'??????ID',r'???????????????',r'??????????????????',r'?????????????????????']]

juese_che = pd.merge(baodan_che,juese_baodan,on=r'??????ID',how='inner')

chezhu_che = juese_che[[r'?????????',r'???????????????']]
toubao_che = juese_che[[r'?????????',r'??????????????????']]
beibao_che = juese_che[[r'?????????',r'?????????????????????']]

lipei_shangzhe = shangzheinfo[[r'??????id',r'???????????????']]


##lipei = pd.read_csv(outdir+'/lipei.csv',encoding='utf8',dtype={0:np.object},nrows=100)
##lipei = lipei[['??????ID','???????????????????????????','?????????']]



##jiashi_che = chesun[['???????????????????????????','?????????']].drop_duplicates()

shigu_che = chesun[[r'??????ID',r'?????????']]

che = baodan[r'?????????'].append(chesun[r'?????????']).drop_duplicates()
jiashiyuan = chesun[r'???????????????????????????'].drop_duplicates()
lipei=chesun[r'??????ID'].drop_duplicates()
toubao = juese[r'??????????????????'].drop_duplicates()
chezhu = juese[r'???????????????'].drop_duplicates()
beibao = juese[r'?????????????????????'].drop_duplicates()
shangzhe = lipei_shangzhe[r'???????????????'].drop_duplicates()

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

che_chezhu = juese_che[['?????????','???????????????']].drop_duplicates().rename(columns={'???????????????':'Target','?????????':'Source'})
che_toubao = juese_che[['?????????','??????????????????']].drop_duplicates().rename(columns={'??????????????????':'Target','?????????':'Source'})
che_beibao = juese_che[['?????????','?????????????????????']].drop_duplicates().rename(columns={'?????????????????????':'Target','?????????':'Source'})
che_jiashiyuan = chesun[['?????????','???????????????????????????']].drop_duplicates().dropna().rename(columns={'???????????????????????????':'Target','?????????':'Source'})
che_lipei=chesun[['?????????','??????ID']].drop_duplicates().rename(columns={'??????ID':'Target','?????????':'Source'})
lipei_shangzhe = lipei_shangzhe.rename(columns={r'??????id':'Target',r'???????????????':'Source'})

edges = pd.concat([che_chezhu,che_toubao,che_jiashiyuan,che_beibao,che_lipei,lipei_shangzhe]).drop_duplicates()
edges.to_csv('./'+outdir+'/edges/source_target.csv',sep=',',index=False)
time_start = time.time()
G=nx.from_pandas_edgelist(edges,'Source','Target')
time_end = time.time()

print('Fill Graph Finished Use Time:',time_end-time_start,'s')
tmpf.write('Fill Graph Finished Use Time:'+str(time_end-time_start)+'s\n')

print('Claim Count:' , len(lipei))
tmpf.write('Claim Count:' + str(len(lipei)) + '\n')

print('Car Count:' , len(che))
tmpf.write('Car Count:' + str(len(che))+ '\n')

print('Car Owner:',len(chezhu))
tmpf.write('Car Owner:'+str(len(chezhu))+'\n')

print('Toubaoren Count:',len(toubao))
tmpf.write('Toubaoren Count:'+str(len(toubao))+'\n')

print('Beibaoren Count:', len(beibao))
tmpf.write('Beibaoren Count:'+ str(len(beibao)) +'\n')

print(r'???????????????:',len(jiashiyuan))
tmpf.write(r'???????????????:'+ str(len(jiashiyuan))+ '\n')

print(r'????????????:',len(shangzhe))
tmpf.write(r'????????????:'+ str(len(shangzhe))+ '\n')

print(r'??????:',len(edges))
tmpf.write('??????:'+str(len(edges))+ '\n')

print('?????????:', len(G.nodes()))
tmpf.write('?????????:'+str(len(G.nodes()))+ '\n')


time_start = time.time()
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

time_end = time.time()
print('Fill Porperties Time:',time_end - time_start,'s')
tmpf.write('Fill Porperties Time:'+str(time_end - time_start)+'s' +  '\n')
time_start = time.time()
partition = community.best_partition(G)
time_end = time.time()
print('Find Partition Time:',time_end-time_start)
tmpf.write('Find Partition Time:'+str(time_end-time_start) +  '\n')

parsize = len(set(partition.values()))
print('Community Count:',parsize)
tmpf.write('Community Count:'+str(parsize) + '\n')
tmpf.close()

edge_list = edges.values.tolist()
procidx = 0

loop_file = codecs.open('./'+outdir+'/loop.csv','w+','utf-8')
loop_writer = csv.writer(loop_file,delimiter=',',quotechar=' ',quoting=csv.QUOTE_MINIMAL)
loop_writer.writerow([r'??????', r'?????????',r'?????????',r'???????????????',r'????????????',r'??????'])
loop_file.flush()
for com in set(partition.values()):
    
    com_nodes = [ nodes for nodes in partition.keys() if partition[nodes] == com]
    node_count = len(com_nodes)
    
    print('proc : ',procidx , '/',parsize,' node_count:',node_count,' id:',com)
    procidx = procidx+1
    
    if node_count < 4 :
        print('\ttoo small passed')
        continue
    if node_count > 100:
        print('\t too large passed')
        continue
    
    dir_name = './'+outdir+'/partitions/' + str(node_count)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    time_start = time.time()
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
    
    time_end = time.time()
    print('\tPrepare Node Files Time:',time_end-time_start)
    time_start = time.time()
        
    lG=nx.Graph()
    lS=nx.Graph()
    for com_node in com_nodes:
        
        node = G.nodes[com_node]
        lG.add_node(com_node)

        if 'lipei' not in node['fenlei']:
            lS.add_node(com_node)
        
        for fenlei in iter(node['fenlei']):
            if fenlei == 'sunshiche':
                sunshiche_writer.writerow([com_node])
                if node['chezhu']:
                    lG.add_node(node['chezhu'])
                    lG.add_edge(com_node,node['chezhu'])
                    lS.add_node(node['chezhu'])
                    lS.add_edge(com_node,node['chezhu'])

                if node['toubao']:
                    lG.add_node(node['toubao'])
                    lG.add_edge(com_node,node['toubao'])
                    lS.add_node(node['toubao'])
                    lS.add_edge(com_node,node['toubao'])

                if len(node['jiashiyuan'])>0:
                    lG.add_nodes_from(list(node['jiashiyuan']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['jiashiyuan'])])
                    lS.add_nodes_from(list(node['jiashiyuan']))
                    lS.add_edges_from([(com_node,other_node) for other_node in iter(node['jiashiyuan'])])

                if len(node['beibao'])>0:
                    lG.add_node(node['beibao'])
                    lG.add_edge(com_node,node['beibao'])
                    lS.add_node(node['beibao'])
                    lS.add_edge(com_node,node['beibao'])

                if len(node['lipei'])>0:
                    lG.add_nodes_from(list(node['lipei']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['lipei'])])
            elif fenlei == 'che':
                che_writer.writerow([com_node])
                if node['chezhu']:
                    lG.add_node(node['chezhu'])
                    lG.add_edge(com_node,node['chezhu'])
                    lS.add_node(node['chezhu'])
                    lS.add_edge(com_node,node['chezhu'])

                if node['toubao']:
                    lG.add_node(node['toubao'])
                    lG.add_edge(com_node,node['toubao'])
                    lS.add_node(node['toubao'])
                    lS.add_edge(com_node,node['toubao'])

                if len(node['beibao'])>0:
                    lG.add_node(node['beibao'])
                    lG.add_edge(com_node,node['beibao'])
                    lS.add_node(node['beibao'])
                    lS.add_edge(com_node,node['beibao'])

                if len(node['jiashiyuan'])>0:
                    lG.add_nodes_from(list(node['jiashiyuan']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['jiashiyuan'])])
                    lS.add_nodes_from(list(node['jiashiyuan']))
                    lS.add_edges_from([(com_node,other_node) for other_node in iter(node['jiashiyuan'])])

                if len(node['lipei'])>0:
                    lG.add_nodes_from(list(node['lipei']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['lipei'])])
            elif fenlei == 'toubao':
                toubao_writer.writerow([com_node])
                if len(node['che'])>0:
                    lG.add_nodes_from(list(node['che']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['che'])])
                    lS.add_nodes_from(list(node['che']))
                    lS.add_edges_from([(com_node,other_node) for other_node in iter(node['che'])])

            elif fenlei=='jiashiyuan':
                jiashiyuan_writer.writerow([com_node])
                if len(node['che'])>0:
                    lG.add_nodes_from(list(node['che']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['che'])])
                    lS.add_nodes_from(list(node['che']))
                    lS.add_edges_from([(com_node,other_node) for other_node in iter(node['che'])])
            elif fenlei=='beibao':
                beibao_writer.writerow([com_node])
                if len(node['che'])>0:
                    lG.add_nodes_from(list(node['che']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['che'])])
                    lS.add_nodes_from(list(node['che']))
                    lS.add_edges_from([(com_node,other_node) for other_node in iter(node['che'])])
                    
            elif fenlei == 'chezhu' :
                chezhu_writer.writerow([com_node])
                if len(node['che'])>0:
                    lG.add_nodes_from(list(node['che']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['che'])])
                    lS.add_nodes_from(list(node['che']))
                    lS.add_edges_from([(com_node,other_node) for other_node in iter(node['che'])])
            elif fenlei == 'shangzhe' :
                shangzhe_writer.writerow([com_node])
                local_shangzhes.append(com_node)
                if len(node['lipei'])>0:
                    lG.add_nodes_from(list(node['lipei']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['lipei'])])
                    lS.add_nodes_from(list(node['lipei']))
                    lS.add_edges_from([(com_node,other_node) for other_node in iter(node['lipei'])])
            elif fenlei == 'lipei':
                lipei_writer.writerow([com_node])
                local_lipeis.append(com_node)
                if len(node['che'])>0:
                    lG.add_nodes_from(list(node['che']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['che'])])
                if len(node['shangzhe'])>0:
                    lG.add_nodes_from(list(node['shangzhe']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['shangzhe'])])


    Gnode_color = []
    for lnode in lG.nodes():
        n = G.nodes[lnode]
        if 'che' in n['fenlei'] :
            Gnode_color.append('blue')
        elif 'shangzhe' in n['fenlei']:
            Gnode_color.append('black')
        elif 'chezhu' in n['fenlei'] :
            Gnode_color.append('green')
        elif 'jiashiyuan' in n['fenlei'] :
            Gnode_color.append('yellow')
        elif 'toubao' in n['fenlei'] :
            Gnode_color.append('red')
        elif 'beibao' in n['fenlei']:
            Gnode_color.append('purple')
        elif 'lipei' in n['fenlei'] :
            Gnode_color.append('cyan')
        else:
            Gnode_color.append('grey')

    Snode_color = []
    for lnode in lS.nodes():
        n = G.nodes[lnode]
        if 'che' in n['fenlei'] :
            Snode_color.append('blue')
        elif 'shangzhe' in n['fenlei']:
            Snode_color.append('black')
        elif 'chezhu' in n['fenlei'] :
            Snode_color.append('green')
        elif 'jiashiyuan' in n['fenlei'] :
            Snode_color.append('yellow')
        elif 'toubao' in n['fenlei'] :
            Snode_color.append('red')
        elif 'beibao' in n['fenlei']:
            Snode_color.append('purple')
        elif 'lipei' in n['fenlei'] :
            Snode_color.append('cyan')
        else:
            Snode_color.append('grey')
    for egs in lG.edges():
        edge_writer.writerow(list(egs))

    hasLoop = False
    needDrop = False
    hasOtherCycle = False 
    try:
        #f1 = nx.algorithms.find_cycle(lG)
        f1 = nx.algorithms.cycle_basis(lG)
        if f1:
            hasLoop = True
            for items in f1:
                #items=set()
                
                #for edge in f1:
                #    ##print(type(edge))
                #    ##print(type(edge[0]))
                #    items.add(edge[0])
                #    items.add(edge[1])
                #print(items)
                #print('numitems', len(items))
                if(len(items)==4):
                    carcount=0
                    personcount=0
                    for item in items:
                        n = G.nodes[item]
                        if 'che' in n['fenlei'] :
                            carcount+=1
                        elif 'jiashiyuan' in n['fenlei']:
                            personcount+=1
                        elif 'toubao' in n['fenlei']:
                            personcount+=1
                        elif 'beibao' in n['fenlei']:
                            personcount+=1
                        elif 'chezhu' in n['fenlei']:
                            personcount+=1
                    print('carcount', carcount,'personcount',personcount)
                    if (carcount == 2 and personcount == 2):
                        if(not hasOtherCycle):
                            needDrop = True
                    else:
                        hasOtherCycle = True
                        needDrop = False
                else:
                    hasOtherCycle = True
                    needDrop = False
    except:
        pass
    print("hasLoop",hasLoop,"needDrop",needDrop,"hasOtherCycle",hasOtherCycle)
    nx.draw_spring(lG,node_color=Gnode_color,with_labels=True)
    ##plt.show()
    plt.savefig(com_dirname + '/figure.png')
    if hasLoop:
        if needDrop:
            plt.savefig('./'+badloopdir+'/' + str(node_count) + '_' + str(com) + '.png')
        else:
            plt.savefig('./'+loopdir+'/' + str(node_count) + '_' + str(com) + '.png')
    plt.clf()
    nx.draw_spring(lG,node_color=Gnode_color)
    plt.savefig(com_dirname + '/figure_nolabel.png')
    if hasLoop:
        if needDrop:
            plt.savefig('./'+badloopdir+'/' + str(node_count) + '_' + str(com) + 'nolabel.png')
        else:
            plt.savefig('./'+loopdir+'/' + str(node_count) + '_' + str(com) + 'nolabel.png')
    plt.clf()

    nx.draw_spring(lS,node_color=Snode_color,with_labels=True)
    ##plt.show()
    plt.savefig(com_dirname + '/nolipei_figure.png')
    plt.clf()
    nx.draw_spring(lS,node_color=Snode_color)
    plt.savefig(com_dirname + '/nolipei_figure_nolabel.png')
    plt.clf()
    lipeinodes='|'.join(local_lipeis)
    locallipeiinfo = lipeiinfo[(lipeiinfo[r'??????ID'].str.contains(lipeinodes))]
    locallipeiinfo.to_csv(com_dirname + r'/???????????????.csv',sep=',',index=False)

    localbaodanxinxi = baodan[(baodan[r'??????ID'].str.contains(lipeinodes))]
    
    if len(localbaodanxinxi) > 0:
        
        localbaodanxinxi.to_csv(com_dirname + r'/???????????????.csv', sep = ',', index=False)
        localbaodanids = localbaodanxinxi[[r'??????ID']].drop_duplicates()[r'??????ID'].tolist()
        localbandanidsstr = '|'.join(localbaodanids)
    
        localjueseinfo = juese[(juese[r'??????ID'].str.contains(localbandanidsstr))]
        localjueseinfo.to_csv(com_dirname + r'/?????????????????????.csv',sep=',',index=False)

        localbaodanhebin = pd.merge(localbaodanxinxi,localjueseinfo,on=r'??????ID',how='inner')
        localbaodanhebin.to_csv(com_dirname + r'/?????????????????????.csv',sep=',',index=False)
    if len(local_shangzhes) > 0:
        shangzhenodes='|'.join(local_shangzhes)
        localrenshang = shangzheinfo[(shangzheinfo[r'??????id'].str.contains(lipeinodes))]
        localrenshang.to_csv(com_dirname + r'/????????????.csv',sep=',',index=False)

    localchesuninfo = chesun[(chesun[r'??????ID'].str.contains(lipeinodes))]
    localchesuninfo.to_csv(com_dirname + r'/????????????.csv',sep=',',index=False)

    localpeifu = peifuinfo[(peifuinfo[r'??????ID'].str.contains(lipeinodes))]
    localpeifu.to_csv(com_dirname + r'/???????????????.csv',sep=',',index=False)

    
    ## id, node_count,lipei_count,lipeijin_e,linjiecount
    linjiecount = len(locallipeiinfo[(locallipeiinfo[r'????????????']==r'??????')])
    #print(com,node_count,len(local_lipeis),locallipeiinfo[[r'????????????']].sum()[0],linjiecount)
    if hasLoop:
        if needDrop:
            loop_writer.writerow([com,node_count,len(local_lipeis),locallipeiinfo[[r'????????????']].sum()[0],linjiecount,1])
        else:
            loop_writer.writerow([com,node_count,len(local_lipeis),locallipeiinfo[[r'????????????']].sum()[0],linjiecount,0])
        loop_file.flush()
    #loop_file.close()

loop_file.close()
    
    
