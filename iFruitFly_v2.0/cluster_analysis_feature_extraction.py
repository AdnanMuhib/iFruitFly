import csv

import fnmatch
import os
import re
from scipy import misc
import numpy as np
import sys

import matplotlib.pyplot as plt

import locale
import cluster_analysis
import segment

locale.setlocale(locale.LC_ALL, "")
locale.setlocale(locale.LC_NUMERIC, "C")

def run():
   # print("Setting folder Path");
    _inputDirectory = input("Please Input the Directory : ");
    #_inputDirectory = "C:\Users\Abdullah Akmal\Documents\Python Scripts\project_testing\Galia\Galia_Day_1";
    #print(_inputDirectory);
    _inputFilter = "*.pgm";
    _inputFilterCSV = "*INFLO.csv";
    _inputFilterMat = "*.mat"
    _inputFileList = [];
    _inputFileCSVList = []
    _inputFileMatList = [];                                                     #only filtered images will be called by the algo

    for r, d, f in os.walk(_inputDirectory):
        for file in fnmatch.filter(f, _inputFilter):
            print("Valid Files are found: ", file);
            _inputFileList.append(os.path.join(r, file));
        for file in fnmatch.filter(f, _inputFilterCSV):
            print("Valid Images are found : ", file);
            _inputFileCSVList.append(os.path.join(r, file));
        for file in fnmatch.filter(f, _inputFilterMat):
            print("Valid Images are found : ", file);
            _inputFileMatList.append(os.path.join(r, file));
        for (c, h, g) in [(c, h, g) for c in _inputFileList for h in _inputFileCSVList for g in _inputFileMatList]:
            #print(re.split('_IR_|.pgm', c)[0]);
            #print(re.split('_INFLO|_csv_|.csv', h)[0]);
            #print(re.split('_IR_|.pgm', c)[1]);
            #print(re.split('_INFLO|_csv_|.csv', h)[1]);
            #print(re.split('_IR_|.pgm', c)[0],re.split('_LOF|_csv_|.csv', h)[0])
            if ((re.split('_IR_|.pgm', c)[0] == re.split('_INFLO|_csv_|.csv', h)[0] == re.split('_Mat_|.mat',g)[0])
                and (re.split('_IR_|.pgm', c)[1] == re.split('_INFLO|_csv_|.csv', h)[1] == re.split('_Mat_|.mat',g)[1])):
               # if(c.split(file,1))
               # imageSegmentor(c, h);
               #print("Entered");
               setup(c, h, g);
    return


def setup(_image, _anamoly,_mat):
    print("Processing Image : ", _image);
    _imageFile = _image;
    _anomalyFile = _anamoly;
    _matFile = _mat
    #_matFile = _mat; 
    _features = cluster_analysis.cluster_analysis(_imageFile, _anomalyFile,_matFile);
    #print(_features,_matFile)
    #print(_points)
    #print(_values)
    if(_features == None):
        print("Image Cant be Segmented due to poor calibration");
        return;
    else:
        imagePloter(_features, _imageFile);
    return

def imagePloter(_feature_data, _im):
    fig = plt.figure();
    fig.add_subplot(1, 2, 1);
    print("Processing Please Wait...");
    im = misc.imread(_im);
    plt.imshow(im);
    n = 1;

    for cluster in _feature_data:
        points = cluster['points'];
        im = np.zeros((480, 640), dtype=int)
        im[points] = cluster['values']
        #plt.figure();
        #plt.imshow(im, cmap='gray')
        print("Writing Images...");
        fig.add_subplot(1, 2, 2);
        plt.imshow(im);
        prefix = re.split('IR_|.pgm', _im)[0];
        #print(prefix);
        postfix = re.split('IR_|.pgm', _im)[1]; 
        #print(postfix);
        plt.savefig(prefix + postfix + "_Cluster_" + str(n) + ".png");
        n = n + 1;
        print("Done..");
    return

def batchProcessor(count):
     print("batch processor file name : cluster_analysis_feature_extraction")
     _count = count;
     if _count == 0:
        run();
        _count = _count + 1;
        batchProcessor(_count);    
     else:
        _in = input("Want to continue?(Y/N) : ");
        if (_in == 'Y'):
            run();
            _count = _count + 1;
            batchProcessor(_count);
        elif (_in == 'N'):
            sys.exit();
        else:
            batchProcessor(_count);     
     return


if __name__ == "__main__":
    batchProcessor(0);
    