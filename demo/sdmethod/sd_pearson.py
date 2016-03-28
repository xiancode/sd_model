#!/usr/bin/env  Python
#-*- coding=utf-8 -*-
'''
Description : statistic indicator pearson coeff
require     : windows Anaconda-2.3.0
author      : shizhongxian@126.com
usage  $python sd_pearson.py  -f table.txt 
'''

import pandas as pd
import numpy as np
import sys
import logging
import os
from optparse import OptionParser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAR_DIR = os.path.dirname(BASE_DIR)

pear_logger = logging.getLogger('SD_API.Method.PEARSON')
pear_logger.setLevel(logging.INFO)
fh = logging.FileHandler(PAR_DIR + os.path.sep + "LOG" + os.path.sep + "SD_PEAR.log")
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
fh.setFormatter(formatter)
pear_logger.addHandler(fh)

def data_set(fname):
    df = pd.read_csv(fname,"\t")
    data = df.rename(columns={'时间':'time','指标':'indicator','数值':'value'})
    pivoted = data.pivot('indicator','time','value')
    #delete empty data
    cleaned_data = pivoted.dropna(axis=0)
    indicators = cleaned_data.index
    indicators = indicators.tolist()
    pear_logger.info("selected indicators:" + " ".join(indicators))
    return cleaned_data,indicators

def sd_pearson(fname,result_name):
    result_dict = {}
    cl_data,indi_list = data_set(fname)
    m,n = cl_data.shape
    if m != 2:
        result_dict['error'] = 'pearson correlation coefficient variable must = 2'
        pear_logger.info("pearson correlation coefficient variable must = 2")
        return result_dict
    #描述统计信息
    descrip_statis = []
    descrip_statis.append(indi_list)
    values = cl_data.values
    #均值
    mean = values.mean(axis=1)
    #标准差
    std  = values.std(axis=1)
    mean_list = mean.tolist()
    std_list = std.tolist()
    mean_list = map(lambda x:str(round(x,4)),mean_list)
    std_list  = map(lambda x:str(round(x,4)),std_list)
    descrip_statis.append(mean_list)
    descrip_statis.append(std_list)
    descrip_statis.append([str(n),str(n)])
    mean = mean.reshape(2,1)
    diff = values - mean
    diff_quadratic = np.square(diff)
    #皮尔森系数
    pearson_corr = sum(diff[0]*diff[1])/np.sqrt(sum(diff_quadratic[0])*sum(diff_quadratic[1]))
    result_dict['pearson_corr'] = str(round(pearson_corr,6))
    result_dict['descript_statistics'] = descrip_statis
    if result_name:
        try:
            save_result(result_dict, result_name)
        except Exception,e:
            print e
            pear_logger.info("result save error")
    print result_dict
    return result_dict

def save_result(result_dict,result_name):
    table_col_header = [' ',"均值","标准差","样本数"]
    descript_statistics = result_dict['descript_statistics']
    table = []
    #构造输出的数据表
    if len(table_col_header) == len(descript_statistics):
        for i in range(len(table_col_header)):
            table.append([table_col_header[i]] + descript_statistics[i])
    with open(result_name,"w") as f:
        f.write('pearson_corr' + '\t')
        f.write(str(result_dict['pearson_corr'])+'\n')
        f.write("===============================\n")
        for des_list in table:
            f.write('\t'.join(des_list))
            f.write('\n')
            
if __name__=="__main__":
    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='input',
                         help='filename containing csv convert from rec',
                         default=None)
    (options, args) = optparser.parse_args()
    #inFile = None
    
    if options.input is None:
            inFile = sys.stdin
            #inFile = "INTEGRATED-DATASET.csv"
    elif options.input is not None:
            inFile = options.input
    else:
            print 'No dataset filename specified, system with exit\n'
            sys.exit('System will exit')

    #inFile = "Pearson.txt"
    full_name = os.path.realpath(inFile)
    pos = full_name.find(".txt")
    result_name = full_name[:pos] + "_result.txt"
    sd_pearson(full_name,result_name)
    
    

    
    
    


    