# -*-encoding:utf-8 -*-
#/usr/bin/python3
import pandas as pd
import numpy as np
import os

outdir= r'./Filtered/'
badoutdir = r'./过滤掉数据/'
indir = r'./'

#def ciFLiPei(filename,outdir,badoutdir,indir):
isExists = os.path.exists(outdir)
if not isExists:
    os.makedirs(outdir)

isExists = os.path.exists(badoutdir)
if not isExists:
    os.makedirs(badoutdir)

lipeidata = pd.read_excel(indir + r'理赔信息.xlsx',\
                           dtype={0:object,\
                                  1:object,\
                                  2:object,\
                                  3:object,\
                                  7:object,\
                                  9:object,\
                                  11:object,\
                                  15:object,\
                                  17:object})

print(r'原始数据大小：',len(lipeidata))

lipei_kong = lipeidata[(pd.isnull(lipeidata[r'赔款收款身份证']))\
          | pd.isnull(lipeidata[r'赔付支付账户名']) \
          | pd.isnull(lipeidata[r'赔款支付账号']) ]

print(r'空数据大小：',len(lipei_kong))

lipei_kong.to_csv(badoutdir + r'理赔信息_赔款收款身份证赔付支付账户名赔款支付账号之一为空.csv')

lipeidata =  lipeidata[( ~pd.isnull(lipeidata[r'赔款收款身份证']))\
          & (~ pd.isnull(lipeidata[r'赔付支付账户名'])) \
          & (~ pd.isnull(lipeidata[r'赔款支付账号'])) ]

print(r'去除空数据后始数据大小：',len(lipeidata))

lipei_jine = lipeidata[(pd.isna(lipeidata[r'赔付金额'])) \
          | (lipeidata[r'赔付金额']<=0)]
print(r'金额问题数据大小：',len(lipei_jine))
lipei_jine.to_csv(badoutdir + r'理赔信息_金额小于0.csv')
                       

lipeidata = lipeidata[ ( ~ pd.isna(lipeidata[r'赔付金额'])) \
          & (lipeidata[r'赔付金额']>0)]
print(r'去除金额问题后数据大小：',len(lipeidata))
                       
lipei_zhifuzhanghu = lipeidata[(~ pd.isna(lipeidata[r'赔付支付账户名'])) \
          & (lipeidata[r'赔付支付账户名'].str.contains('法院|长安|保险')) \
         ]
lipei_zhifuzhanghu.to_csv(badoutdir + r'理赔信息_法院长安保险.csv')
                       
print(r'理赔支付账户问题数据：',len(lipei_zhifuzhanghu))
lipeidata = lipeidata[( pd.isna(lipeidata[r'赔付支付账户名'])) \
         | (~ lipeidata[r'赔付支付账户名'].str.contains('法院|长安|保险'))]
print(r'去除理赔支付账户问题后数据大小：',len(lipeidata))



lipeishoukuanshenfenzhengwenti = lipeidata[ (lipeidata[r'赔款收款身份证'].map(len)<9)]
lipeishoukuanshenfenzhengwenti.to_csv(badoutdir + r'理赔信息_赔款收款身份证长度小于9.csv')
print(r'赔款收款身份证长度小于9数据大小：',len(lipeishoukuanshenfenzhengwenti))
for index, row in lipeishoukuanshenfenzhengwenti.iterrows():
    lipeidata.loc[index,r'赔款收款身份证'] = ''

lipeishangzhezhengjianhaowenti = lipeidata[ (~pd.isna(lipeidata[r'伤者证件号'])) ]
lipeishangzhezhengjianhaowenti = lipeishangzhezhengjianhaowenti[(lipeishangzhezhengjianhaowenti[r'伤者证件号'].map(len)<15)]
lipeishangzhezhengjianhaowenti.to_csv(badoutdir + r'理赔信息_伤者证件号长度小于15.csv')
print(r'伤者证件号长度小于15数据大小：',len(lipeishangzhezhengjianhaowenti))
for index, row in lipeishangzhezhengjianhaowenti.iterrows():
    lipeidata.loc[index,r'伤者证件号'] = ''


lipeidata.to_csv(outdir + r'理赔信息_未删除定损员.csv',index=False)


sort_lipei = lipeidata.sort_values(by=r'报案ID')
sort_lipei.to_csv(outdir + r'理赔信息分组_未删除定损员.csv',index=False)

del lipeidata[r'定损员姓名']
del lipeidata[r'定损员代码']
lipeidata = lipeidata.drop_duplicates()
print(r'删除定损员然后去除重复数据后大小：',len(lipeidata))

lipeidata.to_csv(outdir + r'理赔信息.csv',index=False)


sort_lipei = lipeidata.sort_values(by=r'报案ID')
sort_lipei.to_csv(outdir + r'理赔信息分组.csv',index=False)

#gp_lipei = pd.DataFrame(lipeidata.groupby([r'报案ID',r'立案ID',r'保单ID',r'险种',r'赔付金额',r'赔款收款身份证',r'赔付支付账户名',r'赔款支付账号',r'理赔编码']))
#gp_lipei.to_excel(outdir + r'理赔信息分组.xlsx', sheet_name='Sheet1')
