import os
import re
from simpledbf import Dbf5
import pandas as pd

def getBaseName_noExtension(path):
    return os.path.basename(path).split('.')[0]       

    
def listdir_fullpath(d, regex = None):
    res = []
    for f in os.listdir(d):
        if not regex:
            res.append(os.path.join(d, f))
        else:
            if re.match(regex, f):
                res.append(os.path.join(d, f))    
    return res    


def mkdir_if_not_exist(dirPath):
    if not os.path.isdir(dirPath):
        os.makedirs(dirPath)    




def pd_read_dbf(dbf_path):
    return Dbf5(dbf_path).to_dataframe()
                
def pd_read_shp(shp_path):
    return Dbf5(shp_path.replace('shp','dbf')).to_dataframe()
                

def myjoin(*paths):
    path = ''
    for i in paths:
        path = os.path.join(path, i)
    return path.replace('\\','/')

def path_add(path, addString):
    fullname, suffix = path.split('.')
    return fullname + addString + '.' + suffix    