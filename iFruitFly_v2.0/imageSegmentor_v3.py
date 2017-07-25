# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 15:39:00 2015
Image Segmentation
@author: Abdullah Akmal
"""

#for batch processing
#usage
#input the directory in which you want to run a batch processing
#when the console ask you to enter it


#import fnmatch
import os
#import sys
import re
import fnmatch
import locale
locale.setlocale(locale.LC_ALL, "")
locale.setlocale(locale.LC_NUMERIC, "C")

#for image segmentation

from skimage import color, filters
from skimage.filters import sobel
import numpy as np
from skimage.morphology import watershed
from scipy import misc, io
import matplotlib.pylab as plt
from skimage.util import img_as_ubyte 
import csv
from scipy import fftpack


def batchProcessor():
    #print "";
    print("Setting folder Path");
    
    _inputDirectory = input("Please enter the input directory");
    print(_inputDirectory);
    
    _inputFilter = "*.pgm";
    _inputFilterMat = "*.mat";    
    _inputFileList = [];   
    _inputFileMatList = [];                                                     #only filtered images will be called by the algo    
    
    for r, d, f in os.walk(_inputDirectory):
        for file in fnmatch.filter(f, _inputFilter):
            print("Valid Files are found: ", file);
            _inputFileList.append(os.path.join(r, file));
        for file in fnmatch.filter(f, _inputFilterMat):
            print("Valid Images are found : ", file);
            _inputFileMatList.append(os.path.join(r, file));            
        for (c, h) in [(c, h) for c in _inputFileList for h in _inputFileMatList]:
            #print("printing");            
            #print(re.split('IR_|.pgm', c));
            #print(re.split('Mat_|.mat', h));
            #print(re.split('IR_|.pgm', c));
            #print(re.split('Mat_|.mat', h));
            if ((re.split('IR_|.pgm', c)[0] == re.split('Mat_|.mat', h)[0])
                and (re.split('IR_|.pgm', c)[1] == re.split('Mat_|.mat', h)[1])):
               # if(c.split(file,1))
                imageSegmentor(c, h);
    return


def imageSegmentor(imageFilePath, matFilePath):      
    

    mat = readMatFile(matFilePath);                                             # read mat file                                 
    image = getImage(imageFilePath);                                            # input the image
    typeOfFruit = getTypeOfFruit(image);                                        # on basis of counting or temperature value there are 2 types of fruit

    plt.imshow(image);

    _fft = getFFT(image);
    _mag = getMag(_fft);
    _ang = getAngleInDegrees(_fft);    
     
    edges = edgeDetector(image);                                                # detects the edges of the image
    _segmentation = segmentation(image, typeOfFruit);                           # segments different parts of image    
    filteredImage = filterImageFromSegmentation(image, _segmentation);          # filter the object part of image
    
    outputMatrix = imageMapping(filteredImage, mat['IR']);                      # map the value part of the image and else 0
    
    prefix =  re.split('IR_|.pgm', imageFilePath)[0];
    postfix = re.split('IR_|.pgm', imageFilePath)[1];    
    nameOfFile = prefix + "csv_" 
    nameOfFile = nameOfFile + postfix;
    print(nameOfFile);    
    writeToCSV(outputMatrix, nameOfFile);                                      # write it to the CSV file
    writeFF2CSV(outputMatrix, _mag, _ang, nameOfFile);  
    
    fig, ((fig1, fig2), (fig3, fig4)) = plt.subplots(2, 2, figsize = (10, 8));  # subplot the different plots
    fig1.imshow(image, cmap = plt.cm.gray);                                     # colormap used here is gray    
    fig2.imshow(image, cmap = plt.cm.gray); 
    fig3.imshow(edges, cmap = plt.cm.gray);
    fig4.imshow(filteredImage, cmap = plt.cm.gray);
    
    return

# header file   
def getTypeOfFruit(_image):
   if ((_image[0][0] >  1998) & (_image[0][0] < 70000)):
      _typeOfFruit = 'Counting';
   else:
      _typeOfFruit = 'Temperature';
   return _typeOfFruit;
 
def getImage(_filePath):
    _image = misc.imread(_filePath);
    return _image;
       
def scaler(_imageFile):
    _scaled = color.rgb2gray(_imageFile);     
    return _scaled;

def imageToUnSignedByte(_image):
    _oimage = img_as_ubyte(_image);    
    return _oimage;

def getFFT(_image):
    _fft = np.fft.fft2(_image);    
    return _fft

def getMag(_fft):
    _mag = abs(_fft);
    norm_mag = _mag/_mag.max();
    #angle = angle/angle.max();
    return norm_mag;  
    
def getAngleInDegrees(_fft):
    
    _angle = np.angle(_fft, True);
    _rows, _columns = _fft.shape;
    
    for i in range(0, _rows):
        for j in range(0, _columns):
            if (_angle[i][j] < 0 and abs(_angle[i][j]) <= 180):
                #print(_angle[i][j]);
                #print("\n");
                _angle[i][j] = 180 + _angle[i][j];
                #print(_angle[i][j]);
                #print("\n");
            elif (_angle[i][j] < 0 and abs(_angle[i][j]) > 180):
                #print(_angle[i][j]);
                #print("\n");
                _angle[i][j] = 360 + _angle[i][j];
                #print(_angle[i][j]);
                #print("\n");
    return _angle;    
    
def edgeDetector(_imageFile):
    #_edge = feature.canny((_imageFile/255.), sigma = 3);
    _edge = filters.sobel(_imageFile);
    return _edge 
    
def imageMapping(_img, _imat):
    _rows, _columns = _img.shape;
    for i in range(0, _rows):
        for j in range(0, _columns):
            if _img[i, j] == 0:
                _imat[i][j] = 0;        
    return _imat
    
def writeToCSV(_imat, _nameOfFile):
    _rows, _columns = _imat.shape;
    _array = [];
    _index = 0;
    #_imat.tofile(_nameOfFile + ".csv", sep = ',', format = '%10.5f');    
    #np.savetxt(_nameOfFile + ".csv", _imat, delimiter = ",");
    for i in range(0, _rows):
        for j in range(0, _columns):
            _array.append([]);
            _array[_index].append(i);
            #print(_array[_index]);
            _array[_index].append(j);
            #print(_array[_index]);
            _array[_index].append(_imat[i][j]); 
            #print(_mag[i][j]);
            #_array[_index].append(_mag[i][j]);
            #_array[_index].append(_ang[i][j]);
            #print(_array[_index]); 
            _index = _index + 1;
    writeCSVFile(_array, _nameOfFile + ".csv");
            #np.savetxt(_nameOfFile + ".csv", _array, delimiter = ",", fmt = '%10.5f');
        #_array[_index].tofile(_nameOfFile + ".csv", sep = ',', format = '%10.5f');    
    return
    
def writeFF2CSV(_imat, _mag, _ang, _nameOfFile):
    _rows, _columns = _imat.shape;
    _array = [];
    _index = 0;
    for i in range(0, _rows):
        for j in range(0, _columns):                
            _array.append([]);
            _array[_index].append(i);
            _array[_index].append(j);
            
            if(_imat[i][j] != 0):
                _array[_index].append(_mag[i][j]);
                _array[_index].append(_ang[i][j]);
            elif(_imat[i][j] == 0):
                 _array[_index].append(0);
                 _array[_index].append(0);

            _index = _index + 1;
    writeCSVFile(_array, _nameOfFile + "_FF.csv");        
    return
    
def writeCSVFile(res, csvfile):
    with open(csvfile , "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(res)
    return
    
def segmentation(_image, typeOfFruit):
    #_denoisedImage = rank.median(_image, disk(2));
    #_elevationMap = sobel(_denoisedImage);
    #print(_image);
    _elevationMap = sobel(_image);
    #print(_image);
    _marker = np.zeros_like(_image);
    if (typeOfFruit == 'Counting'):
        _marker[_image < 1998] = 1;
        _marker[_image > 61541] = 2;
    elif (typeOfFruit == 'Temperature'):
        #print("Printing Image");        
        #print(_image < 10);
        _marker[_image < 30] = 1;
        #print(_marker);
        _marker[_image > 150] = 2;
    #_marker = rank.gradient(_denoisedImage, disk(5)) < 10;
    #_marker = ndi.label(_marker)[0];
    #_elevationMap = rank.gradient(_denoisedImage, disk(2));
    _segmentation = watershed(_elevationMap, _marker);
    #print(_segmentation);
    return _segmentation;                
    
def filterImageFromSegmentation(_image, _segmentation):
    _rows, _columns = _image.shape;
    _Image = np.matrix(_image);
    for i in range(0, _rows):
        for j in range(0, _columns):
            if _segmentation[i, j] == 2:
                _Image[i, j] = 0;
    return _Image;
    
def readMatFile(_matFilePath):
    _matrix = io.loadmat(_matFilePath, squeeze_me=True, struct_as_record=False);
    #print(_matrix);
    return _matrix



if __name__ == '__main__':
    batchProcessor();