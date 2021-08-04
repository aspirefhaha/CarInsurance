# -*-encoding:utf-8 -*-
#/usb/bin/python3


from os import replace
import pandas as ks
import community
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import scipy
import time
import os

indir= r'./Filtered/'
outdir=r'./partition'
loopdir = r'./loop'
isExists = os.path.exists(outdir)
if not isExists:
    os.makedirs(outdir)

isExists = os.path.exists(loopdir)
if not isExists:
    os.makedirs(loopdir)

# 由于数据量比较大，在测试过程中，可以设置samplenum为一个较小的数，进行代码调试，如果是0的话，会把数据全部读取到内存中    
samplenum=0
if samplenum == 0:
    baodandata = ks.read_csv(indir + r'baodan.csv',
                             dtype={0:object,3:object,7:object,8:object})
    juesedata = ks.read_csv(indir + r'juese.csv',
                             dtype={0:object,2:object,3:object,7:object,8:object})
    chesundata = ks.read_csv(indir + r'chesun.csv')
    zhifudata = ks.read_csv(indir + r'zhifu.csv')
    lipeidata = ks.read_csv(indir + r'renshang.csv')
else:
    baodandata = ks.read_csv(indir + r'baodan.csv',nrows=samplenum,
                             dtype={0:object,3:object,7:object,8:object})
    juesedata = ks.read_csv(indir + r'juese.csv',
                             dtype={0:object,2:object,3:object,7:object,8:object},nrows=samplenum)
    chesundata = ks.read_csv(indir + r'chesun.csv',nrows=samplenum)
    zhifudata = ks.read_csv(indir + r'zhifu.csv',nrows=samplenum)
    lipeidata = ks.read_csv(indir + r'renshang.csv',nrows=samplenum)

# 报案ID-伤员
shangyuan_baoan = lipeidata[[r'理赔ID',r'伤亡人员证件号码']]
shangyuan = shangyuan_baoan[[r'伤亡人员证件号码']].dropna().drop_duplicates()
shangyuan_baoan_rename = shangyuan_baoan.rename(columns={r'伤亡人员证件号码':'Target',r'理赔ID':'Source'})\
                    .dropna().drop_duplicates()
#shangyuan_baoan.count()

# 车架-人
chejia_ren = ks.merge(baodandata,juesedata,on=r'保单ID')
chejia_ren = chejia_ren[[r'保单ID',r'车架号',r'角色类型',r'身份证号']]
# 投保人
toubaoren = chejia_ren[(chejia_ren[r'角色类型']==2)][[r'车架号',r'身份证号']].drop_duplicates().dropna()
chejia_toubaoren_rename = toubaoren.rename(columns={r'身份证号':'Target',r'车架号':'Source'}).drop_duplicates().dropna()
#chejia_toubaoren.count()

# 车主
chejia_chezhu = chejia_ren[(chejia_ren[r'角色类型']==4)][[r'车架号',r'身份证号']].drop_duplicates().dropna()
chejia_chezhu_rename = chejia_chezhu.rename(columns={r'身份证号':'Target',r'车架号':'Source'}).drop_duplicates().dropna()
#chejia_chezhu.count()

# 被保人
chejia_beibaoren = chejia_ren[(chejia_ren[r'角色类型']==3)][[r'车架号',r'身份证号']].drop_duplicates().dropna()
chejia_beibaoren_rename = chejia_beibaoren.rename(columns={r'身份证号':'Target',r'车架号':'Source'}).drop_duplicates().dropna()
#chejia_beibaoren.count()

# 报案ID：是否承保车辆：车架
baoan_chengbao_chejia = chesundata[[r'理赔ID',r'是否承保车辆',r'车架号']]

# 理赔ID-承保车辆车架
baoan_chengbaoche = baoan_chengbao_chejia[(baoan_chengbao_chejia[r'是否承保车辆'] == 1)][[r'理赔ID',r'车架号']]
# 承保车
chengbaoche = baoan_chengbaoche[[r'车架号']].drop_duplicates().dropna()
baoan_chengbaoche_rename = baoan_chengbaoche.rename(columns={r'车架号':'Target',r'理赔ID':'Source'}).drop_duplicates().dropna()
#baoan_chengbaoche_rename.count()
print('chengbaoche Count:',baoan_chengbaoche_rename.count())

# 理赔ID-三者车辆车架
baoan_sanzheche = baoan_chengbao_chejia[(baoan_chengbao_chejia[r'是否承保车辆'] == 0)][[r'理赔ID',r'车架号']]
# 三者车
sanzheche = baoan_sanzheche[[r'车架号']].drop_duplicates().dropna()
baoan_sanzheche_rename = baoan_sanzheche.rename(columns={r'车架号':'Target',r'理赔ID':'Source'}).drop_duplicates().dropna()
#baoan_sanzheche.count()

# 车架-驾驶人
chejia_jiashiren = chesundata[[r'车架号',r'驾驶证号码']]
# 驾驶人
jiashiren = chesundata[[r'驾驶证号码']].drop_duplicates().dropna()
chejia_jiashiren_rename = chejia_jiashiren.rename(columns={r'驾驶证号码':'Target',r'车架号':'Source'}).drop_duplicates().dropna()
#chejia_jiashiren.count()

# 理赔ID-收款身份证
zhifudata = zhifudata[[r'理赔ID',r'收款身份证']]
zhifudata = zhifudata.drop_duplicates().dropna()
baoan_shoukuanren_rename = zhifudata.rename(columns={r'收款身份证':'Target',r'理赔ID':'Source'})

edges = ks.concat([shangyuan_baoan_rename,
                   baoan_shoukuanren_rename,
                   baoan_chengbaoche_rename,
                   baoan_sanzheche_rename,
                   chejia_toubaoren_rename,
                   chejia_chezhu_rename,
                   chejia_beibaoren_rename,
                   chejia_jiashiren_rename
        ]).drop_duplicates()

time_start = time.time()
#G=nx.from_pandas_edgelist(edges.to_pandas(),r'Source',r'Target')
G=nx.from_pandas_edgelist(edges,r'Source',r'Target')
time_end = time.time()
print(r'Build Graph Time:',time_end-time_start)
time_start = time.time()
for n in G.nodes():
    node=G.nodes[n]
    node['fenlei']=set()
    node['shangyuan']=set()
    node['shoukuanren']=set()
    node['chezhu']=set()
    node['toubaoren']=set()
    node['beibaoren']=set()
    node['jiashiren']=set()     # 承保车、三者车 会有 驾驶人 jiashiren 属性
    node['baoan']=set()
    node['chengbaoche']=set()     # 投保人 车主 被保人 会有 投保车 即 chengbaoche属性
                                 # 报案 会有 承保车 chengbaoche 属性
    node['sanzheche']=set()     # 报案 会有 三者车 sanzheche 属性
    node['che']=set()           # 驾驶人 会有 车 che 属性
    
for idx,basy in shangyuan_baoan_rename.iterrows():
    ba=G.nodes[basy['Source']]
    sy=G.nodes[basy['Target']]

    ba['fenlei'].add('baoan')
    ba['shangyuan'].add(basy['Target'])

    sy['fenlei'].add('shangyuan')
    sy['baoan'].add(basy['Source'])

for idx,bazh  in baoan_shoukuanren_rename.iterrows():
    ba=G.nodes[bazh['Source']]
    zh=G.nodes[bazh['Target']]

    ba['fenlei'].add('baoan')
    ba['shoukuanren'].add(bazh['Target'])
    
    zh['fenlei'].add('shoukuanren')
    zh['baoan'].add(bazh['Source'])

for idx,bacbc in baoan_chengbaoche_rename.iterrows():
    ba=G.nodes[bacbc['Source']]
    cbc=G.nodes[bacbc['Target']]

    ba['fenlei'].add('baoan')
    ba['chengbaoche'].add(bacbc['Target'])
    cbc['fenlei'].add('chengbaoche')
    cbc['baoan'].add(bacbc['Source'])


for idx,baszc in baoan_sanzheche_rename.iterrows():
    ba = G.nodes[baszc['Source']]
    ba['fenlei'].add('baoan')
    ba['sanzheche'].add(baszc['Target'])
    szc=G.nodes[baszc['Target']]
    szc['fenlei'].add('sanzheche')
    szc['baoan'].add(baszc['Source'])

for idx,cjtbr in chejia_toubaoren_rename.iterrows():
    cj=G.nodes[cjtbr['Source']]
    cj['fenlei'].add('chengbaoche')
    cj['toubaoren'].add(cjtbr['Target'])
    tbr=G.nodes[cjtbr['Target']]
    tbr['fenlei'].add('toubaoren')
    tbr['chengbaoche'].add(cjtbr['Source'])

for idx,cjcz in chejia_chezhu_rename.iterrows():
    cj=G.nodes[cjcz['Source']]
    cj['fenlei'].add('chengbaoche')
    cj['chezhu'].add(cjcz['Target'])
    cz=G.nodes[cjcz['Target']]
    cz['fenlei'].add('chezhu')
    cz['chengbaoche'].add(cjcz['Source'])

for idx,cjbbr in chejia_beibaoren_rename.iterrows():
    cj = G.nodes[cjbbr['Source']]
    cj['fenlei'].add('chengbaoche')
    cj['beibaoren'].add(cjbbr['Target'])
    bbr = G.nodes[cjbbr['Target']]
    bbr['fenlei'].add('beibaoren')
    bbr['chengbaoche'].add(cjbbr['Source'])

for idx,cjjsr in chejia_jiashiren_rename.iterrows():
    cj = G.nodes[cjjsr['Source']]
    cj['fenlei'].add('che')
    cj['jiashiren'].add(cjjsr['Target'])
    jsr = G.nodes[cjjsr['Target']]
    jsr['fenlei'].add('jiashiren')
    bbr['che'].add(cjjsr['Source'])

time_start = time.time()
partition = community.best_partition(G)
time_end = time.time()
print(r'Find Partition Time:',time_end-time_start)
#print(r'发现社群用时:',time_end-time_start)

parsize = len(set(partition.values()))
print('Community Count:',parsize)
#print(r'子群数:',parsize)

procidx = 0
for com in set(partition.values()):
    
    com_nodes = [ nodes for nodes in partition.keys() if partition[nodes] == com]
    node_count = len(com_nodes)
    
    print('proc : ',procidx , '/',parsize,' node_count:',node_count,' id:',com)
    procidx = procidx+1
    
    if node_count < 10 :
        print('\ttoo small passed')
        continue
    if node_count > 50:

        print('\t too large passed')
        continue
    
    dir_name = outdir + '/' + str(node_count)
    
    com_dirname = dir_name + "/" + str(com)

    local_baoan = []
    local_toubaoren = []
    local_beibaoren = []
    local_chezhu = []
    local_shoukuanren = []
    local_shangyuan = []
    local_chengbaoche =[]
    local_sanzheche = []
    local_che =[]
    local_jiashiren = []

    lG=nx.Graph()
    for com_node in com_nodes:
        node = G.nodes[com_node]
        lG.add_node(com_node)

        for fenlei in iter(node['fenlei']):
            if fenlei == 'baoan':
                local_baoan.append(com_node)
                if len(node['shoukuanren'])>0:
                    lG.add_nodes_from(list(node['shoukuanren']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['shoukuanren'])])

                if len(node['shangyuan'])>0:
                    lG.add_nodes_from(list(node['shangyuan']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['shangyuan'])])

                if len(node['chengbaoche'])>0:
                    lG.add_nodes_from(list(node['chengbaoche']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['chengbaoche'])])

                if len(node['sanzheche'])>0:
                    lG.add_nodes_from(list(node['sanzheche']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['sanzheche'])])

            if fenlei == 'shangyuan':
                local_shangyuan.append(com_node)
                if len(node['baoan'])>0:
                    lG.add_nodes_from(list(node['baoan']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['baoan'])])

            if fenlei == 'shoukuanren':
                local_shoukuanren.append(com_node)
                if len(node['baoan'])>0:
                    lG.add_nodes_from(list(node['baoan']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['baoan'])])

            if fenlei == 'sanzheche':
                local_sanzheche.append(com_node)
                if len(node['baoan'])>0:
                    lG.add_nodes_from(list(node['baoan']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['baoan'])])

            if fenlei == 'chengbaoche':
                local_chengbaoche.append(com_node)
                if len(node['baoan'])>0:
                    lG.add_nodes_from(list(node['baoan']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['baoan'])])
                if len(node['chezhu'])>0:
                    lG.add_nodes_from(list(node['chezhu']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['chezhu'])])
                if len(node['toubaoren'])>0:
                    lG.add_nodes_from(list(node['toubaoren']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['toubaoren'])])
                if len(node['beibaoren'])>0:
                    lG.add_nodes_from(list(node['beibaoren']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['beibaoren'])])

            if fenlei == 'toubaoren':
                local_toubaoren.append(com_node)
                if len(node['chengbaoche'])>0:
                    lG.add_nodes_from(list(node['chengbaoche']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['chengbaoche'])])

            if fenlei == 'beibaoren':
                local_beibaoren.append(com_node)
                if len(node['chengbaoche'])>0:
                    lG.add_nodes_from(list(node['chengbaoche']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['chengbaoche'])])

            if fenlei == 'chezhu':
                local_chezhu.append(com_node)
                if len(node['chengbaoche'])>0:
                    lG.add_nodes_from(list(node['chengbaoche']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['chengbaoche'])])

            if fenlei == 'jiashiren':
                local_jiashiren.append(com_node)
                if len(node['che'])>0:
                    lG.add_nodes_from(list(node['che']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['che'])])

            if fenlei == 'che':
                local_che.append(com_node)
                if len(node['jiashiren'])>0:
                    lG.add_nodes_from(list(node['jiashiren']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['jiashiren'])])
        

    hasLoop = False
    hasMultiLoop = False
    try:
        #f1 = nx.algorithms.find_cycle(lG)
        f1 = nx.algorithms.cycle_basis(lG)
        if f1:
            hasLoop = True
            if(len(f1)>1): # 大于一个环
                hasMultiLoop = True
            else:
                for items in f1:
                    if(len(items)<5):
                        hasLoop = False
                        
    except Exception as e:
        #print("！！！！！！！！！！！Get Except ",e)
        hasLoop = False
    if(hasLoop):
    #if True:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        if not os.path.exists(com_dirname):
            os.makedirs(com_dirname)
        Gnode_color = []
        for lnode in lG.nodes():
            n = G.nodes[lnode]
            if 'baoan' in n['fenlei'] :
                Gnode_color.append('blue')
            elif 'chengbaoche' in n['fenlei']:
                Gnode_color.append('black')
            elif 'sanzheche' in n['fenlei'] :
                Gnode_color.append('green')
            elif 'che' in n['fenlei'] :
                Gnode_color.append('yellow')
            elif 'shangyuan' in n['fenlei']:
                Gnode_color.append('cyan')
            elif 'jiashiren' in n['fenlei'] :
                Gnode_color.append('pink')
            elif 'chezhu' in n['fenlei'] :
                Gnode_color.append('orange')
            elif 'toubaoren' in n['fenlei'] :
                Gnode_color.append('red')
            elif 'beibaoren' in n['fenlei']:
                Gnode_color.append('purple')
            elif 'shoukuanren' in n['fenlei']:
                Gnode_color.append('gray')
            else:   # 无关
                Gnode_color.append('white')
        nx.draw_spring(lG,node_color=Gnode_color,with_labels=True,node_size=128,font_size=14)
        plt.savefig(com_dirname + '/figure.png')
        if(hasLoop):
            plt.savefig(loopdir+'/' + str(node_count) + '_' + str(com) + '.png')
        plt.clf()
        nx.draw_spring(lG,node_color=Gnode_color,with_labels=False,node_size=128,font_size=14)
        plt.savefig(com_dirname + '/figure_nolabel.png')
        if(hasLoop):
            plt.savefig(loopdir+'/' + str(node_count) + '_' + str(com) + 'nolabel.png')
        plt.clf()
        ks.DataFrame(local_baoan).to_csv(com_dirname + '/local_baoan.csv',index=False,header=0)
        ks.DataFrame(local_toubaoren).to_csv(com_dirname + '/local_toubaoren.csv',index=False,header=0)
        ks.DataFrame(local_beibaoren).to_csv(com_dirname + '/local_beibaoren.csv',index=False,header=0)
        ks.DataFrame(local_chezhu).to_csv(com_dirname + '/local_chezhu.csv',index=False,header=0)
        ks.DataFrame(local_shoukuanren).to_csv(com_dirname + '/local_shoukuanren.csv',index=False,header=0)
        ks.DataFrame(local_shangyuan).to_csv(com_dirname + '/local_shangyuan.csv',index=False,header=0)
        ks.DataFrame(local_chengbaoche).to_csv(com_dirname + '/local_chengbaoche.csv',index=False,header=0)
        ks.DataFrame(local_sanzheche).to_csv(com_dirname + '/local_sanzheche.csv',index=False,header=0)
        ks.DataFrame(local_che).to_csv(com_dirname + '/local_che.csv',index=False,header=0)
        ks.DataFrame(local_jiashiren).to_csv(com_dirname + '/local_jiashiren.csv',index=False,header=0)
        nx.to_pandas_edgelist(lG).to_csv(com_dirname + '/edges.csv',index=False,header=False)
        
        baoans = '|'.join(local_baoan)
        #toubaorens = '|'.join(local_toubaoren)
        #beibaorens = '|'.join(local_beibaoren)
        #chezhus = '|'.join(local_chezhu)

        if(len(local_baoan)>0):    
            local_chesundata = chesundata[(lipeidata[r'理赔ID'].str.contains(baoans))]
            local_zhifudata = zhifudata[(chesundata[r'理赔ID'].str.contains(baoans))]
            local_lipeidata = lipeidata[(chesundata[r'理赔ID'].str.contains(baoans))]
            local_chesundata.to_csv(com_dirname + r'/车损.csv',sep=',',index=False)
            local_zhifudata.to_csv(com_dirname + r'/支付.csv',sep=',',index=False)
            local_lipeidata.to_csv(com_dirname + r'/理赔.csv',sep=',',index=False)
        #if(len(local_chezhu) >0 or len(local_toubaoren)>0 or len(local_beibaoren)>0 ):
        #    local_baodan = baodandata[(baodandata[r'车主证件号'].str.contains(chezhus) |
        #                            baodandata[r'投保人证件号'].str.contains(toubaorens) |
        #                            baodandata[r'被保人证件号'].str.contains(beibaorens) )]
        #    local_baodan.to_csv(com_dirname + r'/保单信息.csv',sep=',',index=False)
