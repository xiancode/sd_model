#!/usr/bin/env  python  
#-*-coding=utf-8-*-
import os
import json

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

if __name__ == "__main__":
    table = file_list(BASE_DIR + "/data/table.txt")
    encodedjson = json.dumps(table)
    print encodedjson