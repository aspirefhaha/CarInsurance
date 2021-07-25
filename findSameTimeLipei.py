# -*-encoding:utf-8 -*-
#/usr/bin/python3

import pandas as pd
import datetime
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
import shutil

outdir = 'fraud_data0602'
suslipeidir = outdir + '/suslipei'

isExists = os.path.exists('./tmpout')
if not isExists:
    os.makedirs('./tmpout')

che = pd.read_csv('./'+outdir+'/nodes/che.csv',encoding='utf-8',sep=',',dtype={0:np.object})
chezhu= pd.read_csv('./'+outdir+'/nodes/chezhu.csv',encoding='utf-8',sep=',',dtype={0:np.object})
toubao= pd.read_csv('./'+outdir+'/nodes/toubao.csv',encoding='utf-8',sep=',',dtype={0:np.object})
jiashiyuan= pd.read_csv('./'+outdir+'/nodes/jiashiyuan.csv',encoding='utf-8',sep=',',dtype={0:np.object})
lipei= pd.read_csv('./'+outdir+'/nodes/lipei.csv',encoding='utf-8',sep=',',dtype={0:np.object})
beibao= pd.read_csv('./'+outdir+'/nodes/beibao.csv',encoding='utf-8',sep=',' ,dtype={0:np.object})
shangzhe= pd.read_csv('./'+outdir+'/nodes/shangzhe.csv',encoding='utf-8',sep=',',dtype={0:np.object})

seldir = './' + outdir + r'/partitions'

lipeidingsunwenti_file = codecs.open('./'+outdir+r'/理赔定损问题_tmp.csv','w+','utf-8')
lipeidingsunwenti_writer = csv.writer(lipeidingsunwenti_file,delimiter=',',quotechar=' ',quoting=csv.QUOTE_MINIMAL)
lipeidingsunwenti_writer.writerow([ r'节点数',r'编号',r'理赔编号',r'时间间隔',r'定损员'])
lipeidingsunwenti_file.flush()

for dir_choose,dirs,files in os.walk(seldir):
    if not dirs:
        print('root',dir_choose)
        if not os.path.exists(dir_choose + '/che.csv'):
            continue
        
        if not os.path.exists(dir_choose + '/che.csv') or os.path.getsize(dir_choose + '/che.csv') == 0:
            lche = []
        else:
            lche = pd.read_csv(dir_choose + '/che.csv',header=None,dtype={0:np.object})[0].tolist()
        
        if not os.path.exists(dir_choose + '/chezhu.csv') or os.path.getsize(dir_choose + '/chezhu.csv') == 0:
            lchezhu = []
        else:
            lchezhu = pd.read_csv(dir_choose + '/chezhu.csv',header=None,dtype={0:np.object})[0].tolist()
        
        if not os.path.exists(dir_choose + '/jiashiyuan.csv') or os.path.getsize(dir_choose + '/jiashiyuan.csv') == 0:
            ljiashiyuan = []
        else:
            ljiashiyuan = pd.read_csv(dir_choose + '/jiashiyuan.csv',header=None,dtype={0:np.object})[0].tolist()
        
        if not os.path.exists(dir_choose + '/lipei.csv') or os.path.getsize(dir_choose + '/lipei.csv') == 0:
            llipei = []
        else:
            llipei = pd.read_csv(dir_choose + '/lipei.csv',header=None,dtype={0:np.object})[0].tolist()
        
        if not os.path.exists(dir_choose + '/sunshiche.csv') or os.path.getsize(dir_choose + '/sunshiche.csv') == 0:
            lsunshiche = []
        else:
            lsunshiche = pd.read_csv(dir_choose + '/sunshiche.csv',header=None,dtype={0:np.object})[0].tolist()
        
        if not os.path.exists(dir_choose + '/toubaoren.csv') or os.path.getsize(dir_choose + '/toubaoren.csv') == 0:
            ltoubaoren = []
        else:
            ltoubaoren = pd.read_csv(dir_choose + '/toubaoren.csv',header=None,dtype={0:np.object})[0].tolist()
        
        if not os.path.exists(dir_choose + '/shangzhe.csv') or os.path.getsize(dir_choose + '/shangzhe.csv') == 0:
            lshangzhe = []
        else:
            lshangzhe = pd.read_csv(dir_choose + '/shangzhe.csv',header=None,dtype={0:np.object})[0].tolist()
        
        if not os.path.exists(dir_choose + '/edges.csv') or os.path.getsize(dir_choose + '/edges.csv') == 0:
            continue
        
        ledges = pd.read_csv(dir_choose + '/edges.csv',sep=' ',header=None,dtype={0:np.object,1:np.object})
        
        lipeiinfo = pd.read_csv(dir_choose + r'/理赔信息表.csv',sep=',',encoding='utf8',dtype={0:np.object,6:np.object,7:np.object,12:np.object,14:np.object,15:np.object})
        chesuninfo = pd.read_csv(dir_choose + r'/车损信息.csv',sep=',',encoding='utf8',dtype={0:np.object,3:np.object,5:np.object,8:np.object})
        
        G=nx.from_pandas_edgelist(ledges,0,1)
        SusLipei = True
        HasLoop = False
        HasTwoLipei = False
        try:
            f1 = nx.algorithms.cycle_basis(G)
            if f1:
                HasLoop = True
                for items in f1:
                    
                    #print(items)
                    #print('numitems', len(items))
                    tlipeis =[]
                    for item in items:
                        if(item in lche):
                            #print("item:" , item , " is Che")
                            pass
                        if(item in lchezhu):
                            #print("item:" , item , " is Chezhu")
                            pass
                        if(item in ljiashiyuan):
                            #print("item:" , item , " is Jiashiyuan")
                            pass
                        if(item in llipei):
                            print("item:" , item , " is Lipei")
                            tlipeis.append(item)
                            pass
                        if(item in lsunshiche):
                            #print("item:" , item , " is Sunshiche")
                            pass
                        if(item in ltoubaoren):
                            #print("item:" , item , " is Toubaoren")
                            pass
                        if(item in lshangzhe):
                            #print("item:" , item , " is Shangzhe")
                            pass
                    if(len(tlipeis)>=2):
                        HasTwoLipei = True
                        #print("lipeis:",tlipeis)
                        lipeistr='|'.join(tlipeis)
                        #print('lipeistr:',lipeistr)
                        complipei = lipeiinfo[(lipeiinfo[r'理赔ID'].str.contains(lipeistr))]
                        lipeishijians = complipei[r'报案时间'].tolist()
                        
                        for i in range(len(lipeishijians)):
                            # if SusLipei == False:
                            #     break
                            baoanshijian = lipeishijians[i]
                            baoanshijianti = datetime.datetime.strptime(baoanshijian,'%Y-%m-%d %H:%M:%S.%f')
                            for j in range(i+1,len(lipeishijians)):
                                duibishijianj = lipeishijians[j]
                                baoanshijiantj = datetime.datetime.strptime(duibishijianj,'%Y-%m-%d %H:%M:%S.%f')
                                difftime = baoanshijianti - baoanshijiantj
                                diffsec = abs(difftime.days * 86400 + difftime.seconds)
                                print("diffsec:",diffsec)
                                if(diffsec > 600):
                                    SusLipei = False
                                    # break
                                else:    
                                    print(r'！！！！！！！！！！！',diffsec)
                                    clipeis = [tlipeis[i] , tlipeis[j]]
                                    tclipeistr = '|'.join(clipeis)
                                    dinsunrens = chesuninfo[(chesuninfo[r'理赔ID'].str.contains(tclipeistr))][r'定损员姓名'].drop_duplicates().tolist()
                                    if(len(dinsunrens)<2):
                                        print(r'**************',dinsunrens)
                                        choosepaths = dir_choose.split('\\')
                                        lipeidingsunwenti_writer.writerow([choosepaths[1],choosepaths[2],tclipeistr,diffsec,dinsunrens[0]])
                                        lipeidingsunwenti_file.flush()
                                    else:
                                        SusLipei = False
                                        # break                        
            else:
                HasLoop = False                        

        except Exception as e:
            print(e)
            print('except')
            pass
        # if(HasLoop and HasTwoLipei and SusLipei):
        #     choosepaths = dir_choose.split('\\')
        #     sourcefilename = outdir + r'/loops/' + choosepaths[1] + r'_' + choosepaths[2] + r'.png'
        #     targetfilename = outdir + r'/suslipei/' + choosepaths[1] + r'_' + choosepaths[2] + r'.png'
        #     if os.path.exists(sourcefilename):
        #         shutil.move(sourcefilename,targetfilename)
        #     sourcefilename = outdir +r'/badloops/' + choosepaths[1] + r'_' + choosepaths[2] + r'.png'
        #     targetfilename = outdir + r'/suslipei/' + choosepaths[1] + r'_' + choosepaths[2] + r'.png'
        #     if os.path.exists(sourcefilename):
        #         shutil.move(sourcefilename,targetfilename)
        #     sourcefilename = outdir+r'/loops/' + choosepaths[1] + r'_' + choosepaths[2] + r'nolabel.png'
        #     targetfilename = outdir + r'/suslipei/' + choosepaths[1] + r'_' + choosepaths[2] + r'nolabel.png'
        #     if os.path.exists(sourcefilename):
        #         shutil.move(sourcefilename,targetfilename)
        #     sourcefilename = outdir + r'/badloops/' + choosepaths[1] + r'_' + choosepaths[2] + r'nolabel.png'
        #     targetfilename = outdir+ r'/suslipei/' + choosepaths[1] + r'_' + choosepaths[2] + r'nolabel.png'
        #     if os.path.exists(sourcefilename):
        #         shutil.move(sourcefilename,targetfilename)
    else:
        print("else")
lipeidingsunwenti_file.close()
