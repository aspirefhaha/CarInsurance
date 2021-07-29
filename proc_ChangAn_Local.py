# -*-encoding:utf-8 -*-
#/usb/bin/python3


from os import replace
import pandas as ks
import community
import networkx as nx
import time

indir= r'./过滤后数据/'
#spark = SparkSession.builder.getOrCreate()


baodandata = ks.read_csv(indir + r'保单信息.csv')
chesundata = ks.read_csv(indir + r'车损信息.csv')
lipeidata = ks.read_csv(indir + r'理赔信息.csv')

# 报案ID-伤员
shangyuan_baoan = lipeidata[[r'报案ID',r'伤者证件号']].rename(columns={r'伤者证件号':'Target',r'报案ID':'Source'})\
                    .dropna().drop_duplicates()
#shangyuan_baoan.count()

# 报案ID-赔款账号
baoan_peikuanzhanghao = lipeidata[[r'报案ID',r'赔款支付账号']].rename(columns={r'赔款支付账号':'Target',r'报案ID':'Source'})\
                            .dropna().drop_duplicates()
#shangyuan_peikuanzhanghao.count()

# 报案ID：是否承保车辆：车架
baoan_chengbao_chejia = chesundata[[r'报案ID',r'是否承保车辆',r'车架号']]

# 报案ID-承保车辆车架
baoan_chengbaoche = baoan_chengbao_chejia[(baoan_chengbao_chejia[r'是否承保车辆'] == '050')][[r'报案ID',r'车架号']]
# 承保车
chengbaoche = baoan_chengbaoche[[r'车架号']].drop_duplicates().dropna()
baoan_chengbaoche_rename = baoan_chengbaoche.rename(columns={r'车架号':'Target',r'报案ID':'Source'}).drop_duplicates().dropna()
#baoan_chengbaoche_rename.count()

# 报案ID-三者车辆车架
baoan_sanzheche = baoan_chengbao_chejia[(baoan_chengbao_chejia[r'是否承保车辆'] == '010')][[r'报案ID',r'车架号']]
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
# 驾驶员
jiashiyuan = chesundata[[r'驾驶员证件号码']].drop_duplicates().dropna()
chejia_jiashiren_rename = chejia_jiashiren.rename(columns={r'驾驶员证件号码':'Target',r'车架号':'Source'}).drop_duplicates().dropna()
#chejia_jiashiren.count()

# 投保车车架 (级别最低)
toubaoche = baodandata[[r'车架号']].drop_duplicates().dropna()

edges = ks.concat([shangyuan_baoan,
                   baoan_peikuanzhanghao,
                   baoan_chengbaoche_rename,
                   baoan_sanzheche_rename,
                   chejia_toubaoren_rename,
                   chejia_chezhu_rename,
                   chejia_beibaoren_rename,
                   chejia_jiashiren_rename
        ]).drop_duplicates()

time_start = time.time()
G=nx.from_pandas_edgelist(edges.to_pandas(),r'Source',r'Target')
time_end = time.time()

time_start = time.time()
for n in G.nodes():
    node=G.nodes[n]
    node['fenlei']=set()
    node['shangyuan']=set()
    node['zhanghao']=set()
    node['chezhu']=''
    node['toubaoren']=''
    node['beibaoren']=''
    node['jiashiyuan']=set()
    node['baoanid']=set()
    node['toubaoche']=set()
    node['chengbaoche']=set()
    node['sanzheche']=set()
    
for idx,basy in shangyuan_baoan.iterrows():
    ba=G.nodes[basy['Source']]
    sy=G.nodes[basy['Target']]

    ba['fenlei'].add('baoan')
    ba['shangyuan'].add[basy['Target']]

    sy['fenlei'].add('shangyuan')
    sy['baoanid'].add(basy['Source'])

for idx,bazh  in baoan_peikuanzhanghao.iterrows():
    ba=G.nodes[bazh['Source']]
    zh=G.nodes[bazh['Target']]

    ba['fenlei'].add('baoan')
    ba['zhanghao'].add(bazh['Target'])
    
    zh['fenlei'].add('zhanghao')
    zh['baoanid'].add(bazh['Source'])

for idx,bacbc in baoan_chengbaoche_rename.iterrows():
    ba=G.nodes[bacbc['Source']]
    cbc=G.nodes[bacbc['Target']]

    ba['fenlei'].add('baoan')
    ba['beibao']=cb['Target']
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
