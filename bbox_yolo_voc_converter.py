import myBasics as mb
import shutil    
import cv2    
import os  

'''
bbox:  xmin, ymin, xmax, ymax
yolo:  centroid.x  centroid.y, object_w, object_h


Example:
#A image whose shape (640, 640). 
# It contain only one object, whose class_id is 0.

# Yolo label   
0  0.32109375  0.496875  -0.0703125  -0.040625 

# bbox label   
1 
228 183 331 305

# VOC label    
0 228 183 331 305

'''



 
def yolo2bbox(imageShape, yoloBox):
    x, y, w, h = yoloBox
    img_w, img_h = imageShape

    x = x*img_w
    w = w*img_w
    y = y*img_h
    h = h*img_h
    bbox = [ int(x-w/2), int(x+w/2), int(y-h/2), int(y+h/2) ]
    return bbox        
        

def fetch_images_bboxLabels_from_trainList(togo_img_dir, togo_label_bbox_dir, trainListTxt, whole_bbox_label_dir):    
    
    with open(trainListTxt, 'r') as f:
        for img_path in f:
            img_path = img_path.strip()
            img_name = os.path.basename(img_path.strip())
            label_path = os.path.join(whole_bbox_label_dir, img_name.replace('JPEG','txt'))        
            shutil.copy(img_path, togo_img_dir)
            shutil.copy(label_path, togo_label_bbox_dir)       


def bbox2yolo_converter(imageShape, bbox):  # xmin, ymin, xmax, ymax
    dw = 1./imageShape[0]
    dh = 1./imageShape[1]
    xmin, ymin, xmax, ymax = bbox
    centroid_x = (xmin + xmax)/2.0
    centroid_y = (ymin + ymax)/2.0
    w = xmax - xmin
    h = ymax - ymin
    x = centroid_x*dw
    y = centroid_y*dh
    w = w*dw
    h = h*dh
    return (x,y,w,h)  #centroid x,y.   object w,h

 
    
    
    
    
def bbox2yolo(bbox_label_path, YOLO_label_path, image_path, class_index):
 
    img_shape = cv2.imread(image_path).shape[:2]
    with open(bbox_label_path, 'r') as f_bbox_label:
        num_text = f_bbox_label.readline()
        #print bbox_label_path
        if num_text:
            boxNum = int(num_text.strip())
            with open(YOLO_label_path, 'w') as f_YOLO_label:
                for i in range(boxNum):
                    lineContent = f_bbox_label.readline().strip()
                    bbox = [int(i) for i in lineContent.split(' ')]
                    bbox = [639 if i>639 else i for i in bbox ]
        
                    yolo_box = bbox2yolo_converter(imageShape=img_shape, bbox=bbox)
                    yolo_box_str = ' '.join([str(i) for i in yolo_box])
                    # print (os.path.basename(YOLO_label_path))
                    # print(bbox)
                    # print (yolo_box)
                    # print ('----------------------------------')
                    
                    f_YOLO_label.write('{}'.format(class_index)+ yolo_box_str + '\n')
        else:
            print ('the bounding box label file is empty')
       
 

            
def bbox2voc(bboxLabelPath, ssdLabelPath, class_index):
    with open(bbox_label_path, 'r') as f_bbox_label:
        num_text = f_bbox_label.readline()
        if num_text:
            boxNum = int(num_text.strip())
            with open(ssd_label_path, 'w') as f_ssd_label:
                for i in range(boxNum):
                    lineContent = f_bbox_label.readline().strip()
                    bbox = [int(i) for i in lineContent.split(' ')]
                    bbox = [639 if i>639 else i for i in bbox ]
                    box_voc_str = ' '.join([str(i) for i in bbox])
 
                    #print bbox
                    f_ssd_label.write('{} '.format(class_index) + box_voc_str + '\n')
        else:
            print ('the bounding box label file is empty')






        
        
        

import numpy as np


# you need provide yoloTrainList.txt file and  the label folder

# your trainlist txt.  contain the paths for each image
yoloTrainListTxt = r'H:\ColonyOutput2_0911_MergeOne-Copy_SPLIT\v1_v2_labelled\forSSD\trainList_0.125.txt'
# the file containing the bounding box label using this tool https://github.com/puzzledqs/BBox-Label-Tool
whole_bbox_label_dir = r'H:\ColonyOutput2_0911_MergeOne-Copy_SPLIT\v1_v2_labelled\labels_bbox'




# it will generate folders for
parentFolder = r'H:\ColonyOutput2_0911_MergeOne-Copy_SPLIT\v1_v2_labelled\forSSD\0.125_test'
togo_img_dir =  os.path.join(parentFolder, 'Images_0.125')
togo_label_bbox_dir = os.path.join(parentFolder, 'Labels_bbox_0.125_NEW')
togo_label_SSD_dir =  os.path.join(parentFolder, 'Labels_SSD_0.125_NEW')
togo_label_YOLO_dir = os.path.join(parentFolder, 'Labels_YOLO_0.125_NEW')

mb.mkdir_if_not_exist(togo_img_dir)
mb.mkdir_if_not_exist(togo_label_bbox_dir)
mb.mkdir_if_not_exist(togo_label_SSD_dir)
mb.mkdir_if_not_exist(togo_label_YOLO_dir)

# fetch image and label(bbox)
fetch_images_bboxLabels_from_trainList(togo_img_dir, togo_label_bbox_dir, yoloTrainListTxt, whole_bbox_label_dir)
 

# sort the list to make sure each image matches each label
sorted_imagePaths_list = list(np.sort(mb.listdir_fullpath(togo_img_dir)))    
sorted_bboxLabels_list = list(np.sort(mb.listdir_fullpath(togo_label_bbox_dir)))    
 

# convert bbox to voc and yolo
# This only due label with one class
# you might need to modify it, if you have more than one classes    

# convert bbox to voc, 
for bbox_label_path in mb.listdir_fullpath(togo_label_bbox_dir):
    bbox_label_filename = os.path.basename(bbox_label_path)
    ssd_label_path = os.path.join(togo_label_SSD_dir, bbox_label_filename) 
    bbox2voc(bbox_label_path, ssd_label_path, class_index=0)
        
        
# convert bbox to yolo    
for image_path, bbox_label_path in zip(sorted_imagePaths_list, sorted_bboxLabels_list):
    bbox_label_filename = os.path.basename(bbox_label_path)
    YOLO_label_path = os.path.join(togo_label_YOLO_dir, bbox_label_filename) 
    bbox2yolo(bbox_label_path, YOLO_label_path, image_path, class_index=0)
        


 
 


    



                 
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    

