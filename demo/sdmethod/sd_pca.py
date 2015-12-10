#!/usr/bin/env  Python
#-*- coding=utf-8 -*-
'''
Description : statistic indicator area ranks by Principal Component Analysis
require     : windows Anaconda-2.3.0
author      : shizhongxian@126.com
usage  $python sd_pca.py  -f table.txt -c 2 
'''


import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn import preprocessing
from optparse import OptionParser
import sys
import logging
import os

#global area_list

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAR_DIR = os.path.dirname(BASE_DIR)

pca_logger = logging.getLogger('SD_API.Method.PCA')
pca_logger.setLevel(logging.INFO)
fh = logging.FileHandler(PAR_DIR + os.path.sep + "LOG" + os.path.sep + "SD_PCA.log")
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
fh.setFormatter(formatter)
pca_logger.addHandler(fh)


def data_set(fname):
    '''
        把数据转化为二维表格,每行表示一个时间段,每列表示一个指标
        删除包含空值的行
    '''
    df = pd.read_csv(fname,"\t")
    #data = df.rename(columns={'月份顺序排序':'m_order','正式指标':'indicator','正式数值':'value'})
    data = df.rename(columns={'地区':'area','正式指标':'indicator','正式数值':'value'})
    
    pivoted = data.pivot('area','indicator','value')
    #删除空值行
    cleaned_data = pivoted.dropna(axis=0)
    areas = cleaned_data.index
    area_list = areas.tolist()
    pca_logger.info("selected area:" + " ".join(area_list))
    
    return cleaned_data,area_list

def sd_pca(fname,components,result_name):
    '''
    pca 计算
    '''
    pca_logger.info("start sd_pca")
    result_dict = {}
    cl_data,area_list = data_set(fname)
    values = cl_data.values
    pca = PCA(n_components=components)
    #数据标准化
    values = preprocessing.scale(values)
    pca.fit(values)
    
    #print(pca.explained_variance_)
    #print(pca.explained_variance_ratio_)
    #print(pca.n_components)
    #print(pca.components_)
    variance_ratio_ = pca.explained_variance_ratio_
    scores = np.dot(pca.transform(values),pca.explained_variance_ratio_)
    scores_list = scores.tolist()
    
    indicators = cl_data.columns
    indi_list = indicators.tolist()
    
    pca_logger.info("cleaned  area:"+" ".join(area_list))
    pca_logger.info("selected indi:"+" ".join(indi_list))
    result_col =  cl_data.columns
    result_col.name = "指标"
    result_idx = ["主成分"+str(i+1) for i in range(components)]
    result_data = pd.DataFrame(pca.components_,columns=result_col,index=result_idx)
    table_1 = []
    table_1.append(list(result_col.values))
    table_1 += result_data.values.tolist()
    result_dict['table_1'] = table_1
    if result_name:
        result_data.to_csv(result_name,sep="\t",float_format='%8.4f')
        fout = open(result_name,"a")
        fout.write("\n===============================\n")
    
    table_2 = []
    for i in range(len(result_idx)):
        if result_name:
            fout.write("%s,\t %.3f \n" %(result_idx[i],variance_ratio_[i]))
        table_2.append(["%s" % result_idx[i],"%.3f" % variance_ratio_[i] ])
    result_dict['table_2'] = table_2
    if result_name:
        fout.write("\n===============================\n")
    rank_1 = []
    if len(area_list) == len(scores):
        area_scores = zip(scores_list,area_list)
        as_dict = dict((key,value) for key,value in area_scores)
        scores_list.sort(reverse=True)
        for score in scores_list:
            if result_name:
                fout.write("%s,%.5f \n" % (as_dict[score],score))
            rank_1.append(["%s" % as_dict[score],"%.5f" % score ])
        result_dict["rank_1"] = rank_1
    else:
        print "caculated result not equal to area_list"
    if result_name:
        fout.close()
        print "save to pca_result.txt"
    return result_dict
    
    
if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='input',
                         help='filename containing csv convert from rec',
                         default=None)
    optparser.add_option('-c', '--components',
                         dest='components',
                         help='factor analysis factors',
                         default=2,
                         type='int')
    
    (options, args) = optparser.parse_args()
    
    
    if options.input is None:
            inFile = sys.stdin
            inFile = 'PCApython2015113092218.txt'
    elif options.input is not None:
            inFile = options.input
    else:
            print 'No dataset filename specified, system with exit\n'
            sys.exit('System will exit')
    components = options.components
    full_name = os.path.realpath(inFile)
    pos = full_name.find(".txt")
    result_name = full_name[:pos] + "_result.txt"
    result_dict = sd_pca(inFile,components,result_name=None)
    pass
    
    
    
    
    


