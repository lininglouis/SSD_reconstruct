import numpy as np
import os
import re
import random
from PIL import Image


def listdir_fullpath(d, regex=None):
  res = []
  for f in os.listdir(d):
    if not regex:
      res.append(os.path.join(d, f))
    else:
      if re.match(regex, f):
        res.append(os.path.join(d, f))
  return res

def chechkLabelImage(imageDir, labelDir):
  image_num = len(listdir_fullpath(imageDir))
  label_num = len(listdir_fullpath(labelDir))
  if image_num != label_num:
    raise ValueError('Error, Images num and Label num dont match!')

def chainJoin(*paths):
  path = ''
  for pathElement in paths:
    path = os.path.join(path, pathElement)
  return path



redo=1
data_dir =  r'F:\AWS\SSD_understand\home\ubuntu\data'
caffe_dir = r'F:\AWS\SSD_understand\home\ubuntu\caffe'

data_dir =  r'/home/ubuntu/data'
caffe_dir = r'/home/ubuntu/caffe'

dataset_name = 'colony'
mapfile= chainJoin(caffe_dir, 'data', dataset_name, 'labelmap_voc.prototxt')

anno_type="detection"
db="lmdb"
min_dim=0
max_dim=0
width=0
height=0

extra_cmd="--encode-type=jpg --encoded"
if redo:
  extra_cmd="$extra_cmd --redo"

for subset in ['test', 'trainval']:
  create_annoset_path = chainJoin(caffe_dir, 'scripts', 'create_annoset.py')
  cmds = 'python  {0} --anno-type={1} --label-map-file={2} --min-dim={3} --max-dim={4} --resize-width={5} --resize-height={6} --check-label {7}       {8}       {9}                                                           {10}             {11}'.format(
     create_annoset_path,     anno_type,            mapfile,      min_dim,    max_dim ,           width,                height,       extra_cmd,    data_dir,   chainJoin(caffe_dir, 'data', dataset_name, subset+'.txt'),     chainJoin(caffe_dir, 'data', dataset_name, db, dataset_name+'_'+subset+'_'+db),  chainJoin('examples', dataset_name)
  )
  os.system(cmds)



