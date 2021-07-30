# -*-encoding:utf-8 -*-
#/usb/bin/python3


from os import replace
import pandas as ks
import community
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time
import os

indir= r'./Filtered/'
#spark = SparkSession.builder.getOrCreate()

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
    baodandata = ks.read_csv(indir + r'baodan.csv')
    chesundata = ks.read_csv(indir + r'chesun.csv')
    lipeidata = ks.read_csv(indir + r'lipei.csv')
else:
    baodandata = ks.read_csv(indir + r'baodan.csv',nrows=samplenum)
    chesundata = ks.read_csv(indir + r'chesun.csv',nrows=samplenum)
    lipeidata = ks.read_csv(indir + r'lipei.csv',nrows=samplenum)

# 报案ID-伤员
shangyuan_baoan = lipeidata[[r'报案ID',r'伤者证件号']]
shangyuan = shangyuan_baoan[[r'伤者证件号']].dropna().drop_duplicates()
shangyuan_baoan_rename = shangyuan_baoan.rename(columns={r'伤者证件号':'Target',r'报案ID':'Source'})\
                    .dropna().drop_duplicates()
#shangyuan_baoan.count()

# 报案ID-赔款账号
baoan_zhanghao = lipeidata[[r'报案ID',r'赔款支付账号']]
zhanghao = baoan_zhanghao[[r'赔款支付账号']].dropna().drop_duplicates()
baoan_zhanghao_rename = baoan_zhanghao.rename(columns={r'赔款支付账号':'Target',r'报案ID':'Source'})\
                            .dropna().drop_duplicates()
#shangyuan_peikuanzhanghao.count()

# 报案ID：是否承保车辆：车架
baoan_chengbao_chejia = chesundata[[r'报案ID',r'是否承保车辆',r'车架号']]

# 报案ID-承保车辆车架
baoan_chengbaoche = baoan_chengbao_chejia[(baoan_chengbao_chejia[r'是否承保车辆'] == 50)][[r'报案ID',r'车架号']]
# 承保车
chengbaoche = baoan_chengbaoche[[r'车架号']].drop_duplicates().dropna()
baoan_chengbaoche_rename = baoan_chengbaoche.rename(columns={r'车架号':'Target',r'报案ID':'Source'}).drop_duplicates().dropna()
#baoan_chengbaoche_rename.count()
print('chengbaoche Count:',baoan_chengbaoche_rename.count())

# 报案ID-三者车辆车架
baoan_sanzheche = baoan_chengbao_chejia[(baoan_chengbao_chejia[r'是否承保车辆'] == 10)][[r'报案ID',r'车架号']]
# 三者车
sanzheche = baoan_sanzheche[[r'车架号']].drop_duplicates().dropna()
baoan_sanzheche_rename = baoan_sanzheche.rename(columns={r'车架号':'Target',r'报案ID':'Source'}).drop_duplicates().dropna()
#baoan_sanzheche.count()

# 车架-投保人
chejia_toubaoren = baodandata[[r'车架号',r'投保人证件号']]
# 投保人
toubaoren = baodandata[[r'投保人证件号']].drop_duplicates().dropna()
chejia_toubaoren_rename = chejia_toubaoren.rename(columns={r'投保人证件号':'Target',r'车架号':'Source'}).drop_duplicates().dropna()
#chejia_toubaoren.count()

# 车架-车主
chejia_chezhu = baodandata[[r'车架号',r'车主证件号']]

# 车主
chezhu = baodandata[[r'车主证件号']].drop_duplicates().dropna()
chejia_chezhu_rename = chejia_chezhu.rename(columns={r'车主证件号':'Target',r'车架号':'Source'}).drop_duplicates().dropna()
#chejia_chezhu.count()

# 车架-被保人
chejia_beibaoren = baodandata[[r'车架号',r'被保人证件号']]
# 被保人
beibaoren = baodandata[[r'被保人证件号']].drop_duplicates().dropna()
chejia_beibaoren_rename = chejia_beibaoren.rename(columns={r'被保人证件号':'Target',r'车架号':'Source'}).drop_duplicates().dropna()
#chejia_beibaoren.count()

# 车架-驾驶人
chejia_jiashiren = chesundata[[r'车架号',r'驾驶员证件号码']]
# 驾驶人
jiashiren = chesundata[[r'驾驶员证件号码']].drop_duplicates().dropna()
chejia_jiashiren_rename = chejia_jiashiren.rename(columns={r'驾驶员证件号码':'Target',r'车架号':'Source'}).drop_duplicates().dropna()
#chejia_jiashiren.count()

# 投保车车架 (级别最低)
toubaoche = baodandata[[r'车架号']].drop_duplicates().dropna()

edges = ks.concat([shangyuan_baoan_rename,
                   baoan_zhanghao_rename,
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
    node['zhanghao']=set()
    node['chezhu']=set()
    node['toubaoren']=set()
    node['beibaoren']=set()
    node['jiashiren']=set()     # 承保车、三者车 会有 驾驶人 jiashiren 属性
    node['baoan']=set()
    node['toubaoche']=set()     # 投保人 车主 被保人 会有 投保车 toubaoche属性
    node['chengbaoche']=set()   # 报案 会有 承保车 chengbaoche 属性
    node['sanzheche']=set()     # 报案 会有 三者车 sanzheche 属性
    node['che']=set()           # 驾驶人 会有 车 che 属性
    
for idx,basy in shangyuan_baoan_rename.iterrows():
    ba=G.nodes[basy['Source']]
    sy=G.nodes[basy['Target']]

    ba['fenlei'].add('baoan')
    ba['shangyuan'].add(basy['Target'])

    sy['fenlei'].add('shangyuan')
    sy['baoan'].add(basy['Source'])

for idx,bazh  in baoan_zhanghao_rename.iterrows():
    ba=G.nodes[bazh['Source']]
    zh=G.nodes[bazh['Target']]

    ba['fenlei'].add('baoan')
    ba['zhanghao'].add(bazh['Target'])
    
    zh['fenlei'].add('zhanghao')
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
    cj['fenlei'].add('toubaoche')
    cj['toubaoren'].add(cjtbr['Target'])
    tbr=G.nodes[cjtbr['Target']]
    tbr['fenlei'].add('toubaoren')
    tbr['toubaoche'].add(cjtbr['Source'])

for idx,cjcz in chejia_chezhu_rename.iterrows():
    cj=G.nodes[cjcz['Source']]
    cj['fenlei'].add('toubaoche')
    cj['chezhu'].add(cjcz['Target'])
    cz=G.nodes[cjcz['Target']]
    cz['fenlei'].add('chezhu')
    cz['toubaoche'].add(cjcz['Source'])

for idx,cjbbr in chejia_beibaoren_rename.iterrows():
    cj = G.nodes[cjbbr['Source']]
    cj['fenlei'].add('toubaoche')
    cj['beibaoren'].add(cjbbr['Target'])
    bbr = G.nodes[cjbbr['Target']]
    bbr['fenlei'].add('beibaoren')
    bbr['toubaoche'].add(cjbbr['Source'])

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
    
    if node_count < 7 :
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

    
    
    lG=nx.Graph()
    for com_node in com_nodes:
        node = G.nodes[com_node]
        lG.add_node(com_node)

        
        for fenlei in iter(node['fenlei']):
            if fenlei == 'baoan':
                local_baoan.append(com_node)

                if len(node['zhanghao'])>0:
                    lG.add_nodes_from(list(node['zhanghao']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['zhanghao'])])

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
                if len(node['baoan'])>0:
                    lG.add_nodes_from(list(node['baoan']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['baoan'])])

            if fenlei == 'zhanghao':
                if len(node['baoan'])>0:
                    lG.add_nodes_from(list(node['baoan']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['baoan'])])

            if fenlei == 'chengbaoche':
                if len(node['baoan'])>0:
                    lG.add_nodes_from(list(node['baoan']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['baoan'])])

            if fenlei == 'sanzheche':
                if len(node['baoan'])>0:
                    lG.add_nodes_from(list(node['baoan']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['baoan'])])

            if fenlei == 'toubaoche':
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
                if len(node['toubaoche'])>0:
                    lG.add_nodes_from(list(node['toubaoche']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['toubaoche'])])

            if fenlei == 'beibaoren':

                local_beibaoren.append(com_node)

                if len(node['toubaoche'])>0:
                    lG.add_nodes_from(list(node['toubaoche']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['toubaoche'])])

            if fenlei == 'chezhu':

                local_chezhu.append(com_node)

                if len(node['toubaoche'])>0:
                    lG.add_nodes_from(list(node['toubaoche']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['toubaoche'])])

            if fenlei == 'jiashiren':
                if len(node['che'])>0:
                    lG.add_nodes_from(list(node['che']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['che'])])

            if fenlei == 'che':
                if len(node['jiashiren'])>0:
                    lG.add_nodes_from(list(node['jiashiren']))
                    lG.add_edges_from([(com_node,other_node) for other_node in iter(node['jiashiren'])])
        

    hasLoop = False
    try:
        #f1 = nx.algorithms.find_cycle(lG)
        f1 = nx.algorithms.cycle_basis(lG)
        if f1:
            hasLoop = True
    except Exception as e:
        print("！！！！！！！！！！！Get Except ",e)
    #if(hasLoop):
    if True:
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
            elif 'toubaoren' in n['fenlei'] :
                Gnode_color.append('red')
            elif 'beibaoren' in n['fenlei']:
                Gnode_color.append('purple')
            elif 'chezhu' in n['fenlei'] :
                Gnode_color.append('orange')
            elif 'jiashiren' in n['fenlei'] :
                Gnode_color.append('pink')
            elif 'shangyuan' in n['fenlei']:
                Gnode_color.append('cyan')
            else:   # zhanghao
                Gnode_color.append('gray')
        nx.draw_spring(lG,node_color=Gnode_color,with_labels=True)
        plt.savefig(com_dirname + '/figure.png')
        if(hasLoop):
            plt.savefig(loopdir+'/' + str(node_count) + '_' + str(com) + '.png')
        plt.clf()
        nx.draw_spring(lG,node_color=Gnode_color,with_labels=False)
        plt.savefig(com_dirname + '/figure_nolabel.png')
        if(hasLoop):
            plt.savefig(loopdir+'/' + str(node_count) + '_' + str(com) + 'nolabel.png')
        plt.clf()

        baoans = '|'.join(local_baoan)
        toubaorens = '|'.join(local_toubaoren)
        beibaorens = '|'.join(local_beibaoren)
        chezhus = '|'.join(local_chezhu)
            
        local_lipeidata = lipeidata[(lipeidata[r'报案ID'].str.contains(baoans))]
        local_chesundata = chesundata[(chesundata[r'报案ID'].str.contains(baoans))]
        local_baodan = baodandata[(baodandata[r'车主证件号'].str.contains(chezhus) |
                                    baodandata[r'投保人证件号'].str.contains(toubaorens) |
                                    baodandata[r'被保人证件号'].str.contains(beibaorens) )]
            
            
        local_lipeidata.to_csv(com_dirname + r'/理赔信息.csv',sep=',',index=False)
        local_chesundata.to_csv(com_dirname + r'/车损信息.csv',sep=',',index=False)
        local_baodan.to_csv(com_dirname + r'/保单信息.csv',sep=',',index=False)

