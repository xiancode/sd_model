#!/usr/bin/env  python  
#-*-coding=utf-8-*-

import json
import os.path
import random
import datetime
from django.utils import  timezone
from django.utils.timezone import utc

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def json_file(json_list,out_fname):
    result_str = ""
    for row in json_list:
        line = "\t".join(row)
        line += "\n"
        result_str += line
    with open(out_fname,"w") as f:
        f.write(result_str.encode("utf8"))        
        
def file_list(in_fname):
    result_list = []
    with open(in_fname) as f:
        for line in  f.readlines():
            line = line.strip()
            line_list = line.split("\t")
            result_list.append(line_list)
    return result_list

def generate_file_from_time(current,dir_name):
    '''
    generate file dir and filename from current time
    '''
    cur_time  = current.strftime('%Y-%m-%d %H-%M-%S')
    [time_dir,time_file] = cur_time.split(" ")
    dir_path = dir_name +os.path.sep +  time_dir
    if os.path.exists(dir_path):
        pass
    else:
        os.mkdir(dir_path)
    random_filename = str(random.random())[2:12]
    file_name = time_file+"-" + random_filename + ".dat"
    full_path = os.path.join(dir_path,file_name)
    return full_path

def generate_file_from_timestr(date_str,time_str,dir_name):
    '''
    generate file dir and filename from current time str
    '''
    dir_path = dir_name +os.path.sep +  date_str
    if os.path.exists(dir_path):
        pass
    else:
        os.mkdir(dir_path)
    random_filename = str(random.random())[2:12]
    file_name = time_str+"-" + random_filename + ".dat"
    full_path = os.path.join(dir_path,file_name)
    return full_path

def get_now_time():
    current = datetime.datetime.utcnow().replace(tzinfo=utc)
    current = timezone.localtime(current)
    result_time = current.strftime('%H-%M-%S')
    return str(result_time).decode()
        
if __name__ == "__main__":
    table = file_list(BASE_DIR + "/data/table.txt")
    encodedjson = json.dumps(table)
    print encodedjson
    
    