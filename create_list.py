import numpy as np
import os
import re
import random
from PIL import Image

def listdir_fullpath(d, regex = None):
    res = []
    for f in os.listdir(d):
        if not regex:
            res.append(os.path.join(d, f))
        else:
            if re.match(regex, f):
                res.append(os.path.join(d, f))    
    return res    

def checkLabelImage(imageDir, labelDir):
    image_num = len(listdir_fullpath(imageDir))
    label_num = len(listdir_fullpath(labelDir))

    imagePathList = listdir_fullpath(imageDir)
    labelPathList = listdir_fullpath(labelDir)
    
    for imgPath, labelPath in zip(listdir_fullpath(imageDir), istdir_fullpath(labelDir)):
        if getFileName_noExtension(imgPath) != getFileName_noExtension(labelPath):
            raise ValueError('Error, Images num and Label num dont match!')
 
    if image_num != label_num:
        raise ValueError('Error, Images num and Label num dont match!')

def getShuffleList(list_data):
    list_ = list_data[:]
    random.seed(42)
    random.shuffle(list_)
    return list_

def splitList(dataList, trainRatio=0.8):
    trainNum = int(round(len(dataList) * trainRatio))
    trainList = dataList[:trainNum]
    testList = dataList[trainNum:]
    return trainList, testList

def getShuffledList(dataList):
    dataSize = len(dataList)
    dataList_shuffled = random.sample(dataList, len(dataList))
    return dataList_shuffled


def getFileName_noExtension(path):
    basename_withExtension = os.path.basename(path)
    filename, extension = os.path.splitext(basename_withExtension)
    return filename

#create a directory under data
dataset = 'colony'

data_root_dir = r'F:\AWS\SSD_understand\home\ubuntu\data\colony'
data_root_dir = os.path.join(r'/home/ubuntu/data', dataset)


images_relative_dir = os.path.join(dataset, 'Images')
labels_relative_dir = os.path.join(dataset, 'Labels')

current_dir= os.getcwd()
print ("current_dir:",  current_dir)
dst_all_tmp= os.path.join(current_dir, "all_tmp.txt")
dst_file_trainval= os.path.join(current_dir, "trainval.txt")
dst_file_test= os.path.join(current_dir, "test.txt")
dst_file_test_name_size= os.path.join(current_dir, "test_name_size.txt")


imageDir = os.path.join(data_root_dir, 'Images')
labelDir = os.path.join(data_root_dir, 'Labels')
checkLabelImage(imageDir, labelDir)

images_list = listdir_fullpath(imageDir)
label_list = listdir_fullpath(labelDir)

images_list.sort()
label_list.sort()
images_labels_pairs = zip(images_list, label_list)
print (images_list[0], label_list[0])
images_labels_pairs_shuffled = getShuffleList(images_labels_pairs)
trainval_pairs, test_pairs = splitList(images_labels_pairs_shuffled, trainRatio=0.8)


with open(dst_file_trainval, 'wb') as f:
    for trainImagePath, trainLabelPath in trainval_pairs:
        trainImageName = os.path.basename(trainImagePath)
        trainLabelName = os.path.basename(trainLabelPath)

        trainRelativeImagesPath = trainImagePath[trainImagePath.find(dataset):]
        trainRelativeLabelsPath = trainLabelPath[trainLabelPath.find(dataset):]
        f.write(trainRelativeImagesPath +  ' ' + trainRelativeLabelsPath + '\n')


with open(dst_file_test, 'wb') as f:
    for testImagePath, testLabelPath in test_pairs:
        testImageName = os.path.basename(testImagePath)
        testLabelName = os.path.basename(testLabelPath)

        testRelativeImagesPath = testImagePath[testImagePath.find(dataset):]
        testRelativeLabelsPath = testLabelPath[testLabelPath.find(dataset):]
        #print testImageName, testLabelName
        f.write(testRelativeImagesPath +  ' ' + testRelativeLabelsPath + '\n')


with open(dst_file_test_name_size, 'wb') as f:
    for testImagePath, testLabelPath in test_pairs:
        testImageName = os.path.basename(testImagePath)
        testImageName_noExtension = getFileName_noExtension(testImageName)

        img = Image.open(testImagePath)
        rows, cols = img.size
        line_txt =  testImageName_noExtension + ' ' + str(rows) + ' ' + str(cols)
        f.write(line_txt + '\n')









