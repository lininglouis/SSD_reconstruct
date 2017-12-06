# SSD_reconstruct <br><br>

This repository do two things.
1. change create_data.sh and create_list.sh two shell scripts in SSD to python version.
2. create a converter between bboundingbox label(https://github.com/puzzledqs/BBox-Label-Tool),  Yolo Label and VOC label.
SSD could read voc txt label.


**Bounding box look like this** <br><br>
object number
xmin, xmax, ymin, ymax
xmin, xmax, ymin, ymax

Example 
2
10 75 44 111
18 151 48 186



**VOC format label look like this** <br><br>
class_id  xmin, xmax, ymin, ymax,  xmin, xmax, ymin, ymax

Example 
0 10 75 44 111  
0 18 151 48 186




**YOLO format label look like this** <br><br>
class_id    obj_centroid_x/img_w  obj_centroid_y/img_h  obj_width    obj_height
0 0.915625 0.31640625 0.1 0.1796875
0 0.721875 0.4390625 0.275 0.134375
0 0.709375 0.30703125 0.171875 0.1234375


**bbox to YOLO converter** <br><br>
since bbox and voc are very similar, the core calculation of the conversion is from bbox to yolo
def bbox2yolo_converter(imageShape, bbox):  #xmin, xmax, ymin, ymax
    dw = 1./imageShape[0]
    dh = 1./imageShape[1]
    xmin, xmax, ymin, ymax = bbox
    centroid_x = (xmin + xmax)/2.0
    centroid_y = (ymin + ymax)/2.0
    w = xmax - xmin
    h = ymax - ymin
    x = centroid_x*dw
    y = centroid_y*dh
    w = w*dw
    h = h*dh
    return (x,y,w,h)  #centroid x,y.   object w,h





 
