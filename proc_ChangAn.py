# -*-encoding:utf-8 -*-
#/usb/bin/python3


from os import replace
import databricks.koalas as ks
import pandas as pd
import community
import networkx as nx
import time
from pyspark.sql import SQLContext

indir= r'hdfs://172.16.155.180:50069/user/hdfs/Filtered/'
#spark = SparkSession.builder.getOrCreate()
sqlContext=SQLContext(sc)

baodandata = ks.read_csv(indir + r'baodan.csv')
chesundata = ks.read_csv(indir + r'chesun.csv')
lipeidata = ks.read_csv(indir + r'lipei.csv')

pd_baodan = baodandata.to_pandas()
bd_baodan = sc.broadcast(pd_baodan)

pd_chesun = chesundata.to_pandas()
bd_chesun = sc.broadcast(pd_chesun)

pd_lipei = lipeidata.to_pandas()
bd_lipe = sc.broadcast(pd_lipei())


# spark_df = sqlContext.createDataFrame(baodandata)
# sc.broadcast(baodandata)

# 报案ID-伤员
shangyuan_baoan = lipeidata[[r'报案ID',r'伤者证件号']].rename(columns={r'伤者证件号':'Target',r'报案ID':'Source'})
shangyuan_baoan = shangyuan_baoan.dropna().drop_duplicates()
#shangyuan_baoan.count()

# 报案ID-赔款账号
shangyuan_peikuanzhanghao = lipeidata[[r'报案ID',r'赔款支付账号']].rename(columns={r'赔款支付账号':'Target',r'报案ID':'Source'})
shangyuan_peikuanzhanghao = shangyuan_peikuanzhanghao.dropna().drop_duplicates()
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

# 投保车车架
toubaoche = baodandata[[r'车架号']].drop_duplicates().dropna()

edges = ks.concat([shangyuan_baoan,
                   shangyuan_peikuanzhanghao,
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
print(r'Build Graph Time:',time_end-time_start)
time_start = time.time()
for n in G.nodes():
    node=G.nodes[n]
    node['fenlei']=set()
    node['chezhu']=''
    node['toubaoren']=''
    node['jiashiyuan']=set()
    node['baoanid']=set()
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

partition = community.best_partition(G)
