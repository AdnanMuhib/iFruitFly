import os
import fnmatch
import re
import locale
locale.setlocale(locale.LC_ALL, "")
locale.setlocale(locale.LC_NUMERIC, "C")

#for image segmentation

from skimage import color, filters
from skimage.filters import sobel
import numpy as np
from skimage.morphology import watershed, convex_hull_image
from scipy import misc, io
from skimage.util import img_as_ubyte
from scipy import misc


def segment(imageFilePath, matFilePath):

    mat = readMatFile(matFilePath);                                             # read mat file
    image = getImage(imageFilePath);                                            # input the image
    typeOfFruit = getTypeOfFruit(image);                                        # on basis of counting or temperature value there are 2 types of fruit

    #plt.imshow(image);

    edges = edgeDetector(image);                                                # detects the edges of the image
    _segmentation = segmentation(image, typeOfFruit);                           # segments different parts of image
    filteredImage = filterImageFromSegmentation(image, _segmentation);          # filter the object part of image

    outputMatrix = imageMapping(filteredImage, mat['IR']);                      # map the value part of the image and else 0
    outputMatrix = convex_hull_image(outputMatrix.copy(order='C'))
    return (filteredImage,outputMatrix)

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
