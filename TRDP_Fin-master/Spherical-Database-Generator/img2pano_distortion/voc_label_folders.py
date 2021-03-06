# pcl: modified from darknet_AlexeyAB to label VOC datasets accepting path with JPEGImages and Annotation folders, and year

import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import sys

# sets=[('2012', 'train'), ('2012', 'val'), ('2007', 'train'), ('2007', 'val'), ('2007', 'test')]
# sets=[('2007', 'test')]


classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]


def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(year, image_id, path):
    in_file = open(path + '/Annotations/%s.xml'% image_id)
    out_file = open(path + '/labels/%s.txt' % image_id, 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


if __name__ == '__main__':

    path = sys.argv[1]
    year = sys.argv[2]

    if year == '2007':
        sets=['train','val','test']
    if year == '2012':
        sets = ['train', 'val']

    for image_set in sets:
        if not os.path.exists(path + '/labels/'):
            os.makedirs(path + '/labels/')

        image_ids = open(path + '/ImageSets/Main/%s.txt' %  image_set).read().strip().split()
        list_file = open(path + '/%s_%s.txt' % (year, image_set), 'w')
        for image_id in image_ids:
            list_file.write(path + '/JPEGImages/%s.jpg\n' % image_id)
            convert_annotation(year, image_id, path)
        list_file.close()




