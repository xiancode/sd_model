#!/usr/bin/env  Python
#-*- coding=utf-8 -*-
'''
Description : 教育均衡状况--差异系数计算  The coefficient of variation 
require     : windows Anaconda-2.3.0
author      : shizhongxian@126.com
usage  $python sd_edu_coeff.py  -f table.txt 
'''

import pandas as pd
import numpy as np
import sys
import logging
import os
from optparse import OptionParser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAR_DIR = os.path.dirname(BASE_DIR)

educv_logger = logging.getLogger('SD_API.Method.EDU_COEFF')
educv_logger.setLevel(logging.INFO)
fh = logging.FileHandler(PAR_DIR + os.path.sep + "LOG" + os.path.sep + "EDUCV_COEFF.log")
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
fh.setFormatter(formatter)
educv_logger.addHandler(fh)

def data_set(fname):
    df = pd.read_csv(fname,"\t")
    data = df.rename(columns={'地区':'area','正式指标':'indicator','正式数值':'value'})
    pivoted = data.pivot('area','indicator','value')
    indicators = pivoted.columns
    #删除空值行
    cleaned_data = pivoted
    area_list = cleaned_data.index
    return cleaned_data,area_list,indicators
    
def sd_edu_coeff(fname,result_name):
    '''
    参考 '县域义务教育均衡发展计算差异系数模板'
    '''
    result_dict = {}
    try:
        cl_data,area_list,indicators  = data_set(fname)
    except Exception,e:
        educv_logger.error(fname + " load data error:"+str(e))
        sys.exit("occur error")
    #提取在校学生数列
    students = cl_data['在校学生数']
    students_num = list(students)
    #删除在校学生数列,只计算其他指标
    cl_data = cl_data.drop('在校学生数', 1)
    origin_values = cl_data.values
    m,n = origin_values.shape
    #地区总学生数
    student_all_num = sum(students_num)
    #地区学生数均值
    student_all_mean = float(student_all_num)/len(students_num)
    #area_sum各指标地区合计值
    #输出表格的第一列
    area_sum = origin_values.sum(axis=0)
    #地区各指标平均值 为指标值合计/总学生数
    area_mean =  area_sum/float(student_all_num)
    #学生数列表转化为array
    students_arr = np.array(students_num,dtype=float)
    #拷贝学生数列，方便计算
    students_arr_tmp = students_arr.copy()
    students_arr_tmp.resize(m,1)
    xi_t = origin_values/students_arr_tmp
    pi_pn = np.array(students_num)/float(student_all_num)
    pi_pn.resize([10,1])
    indi_w = pi_pn*np.square(xi_t - area_mean)
    s = np.sqrt(indi_w.sum(axis=0))
    s = map(lambda x:round(x,8),s)
    cv = s/area_mean
    complex_cv = cv.mean()
    result_dict['indicator'] = ['在校学生数'] + cl_data.columns.tolist()
    result_dict['area_sum'] = [str(student_all_num)] + map(str,area_sum)
    result_dict['area_mean'] = ['------'] + map(str,area_mean)
    result_dict['s'] = ['------'] + map(str,s)
    result_dict['cv'] = ['------'] + map(str,cv)
    result_dict['complex_cv'] = str(round(complex_cv,6))
    result_dict['order'] = ['indicator','area_sum','area_mean','s','cv']
    if result_name:
        try:
            save_result(result_dict, result_name)
        except Exception,e:
            educv_logger.info("result save error!")
    return  result_dict

def save_result(result_dict,result_name):
    table_col_header = [' ',"地区合计","地区平均值","标准差","差异系数"]
    table = []
    #构造输出的数据表
    if len(table_col_header) == len(result_dict['order']):
        with open(result_name,"w") as f:
            i = 0
            for order_name in result_dict['order']:
                l = result_dict[order_name]
                f.write(table_col_header[i]+"\t")
                i = i+1
                f.write("\t".join(l))
                f.write("\n")
            f.write("综合差异系数\t"+result_dict['complex_cv']+"\n")
    else:
        educv_logger.error("table error:table_col_header is not equal content row!")
        
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
    #inFile = "EDUCoeffpython20163178203.txt"
    full_name = os.path.realpath(inFile)
    pos = full_name.find(".txt")
    result_name = full_name[:pos] + "_result.txt"
    sd_edu_coeff(full_name,result_name)
    
    
    
    
    
    
    
