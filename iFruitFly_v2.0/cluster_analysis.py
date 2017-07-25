import csv
import numpy as np
import matplotlib.pyplot as plt
import os
import re
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from scipy.ndimage import morphology
from skimage.io import imread
from skimage import morphology as skimorph
from skimage import measure
#import pandas as pd
from shutil import copy2

import segment


def myFloat(myList):
    return map(float, myList)


def myInt(myList):
    return map(int, myList)


def getHistFeatureKeys():
    keys = []
    for i in range(0, 32):
        keys.append("hist" + str(i))
    return keys


def takeInput():
    cluster_analysis(_imagefile, _anomalyfile, _matfile);
    return


def cluster_analysis(_imagefile, _anomalyfile, _matfile, write_dir, _junk, file_name, permanent_dir):
    _feature_data = []
    _hist_data = [];
    prefix = re.split('IR_|.pgm', _imagefile)[0];
    # print(prefix);
    postfix = re.split('IR_|.pgm', _imagefile)[1];
    # print(postfix);
    # _image = imread(_imagefile)
    # Get the region properties of the whole fruit
    # We need these to express the properties of anomaly region as ratios
    # of the whole fruit surface
    (_image, mask) = segment.segment(_imagefile, _matfile)
    _image = np.asarray(_image)
    mask = np.asarray(mask)
    mask = mask.astype(int)
    _props = measure.regionprops(mask, _image)
    plt.imshow(_image, cmap='gray')
    plt.close()
    if len(_props) == 0:
        return None
    else:
        _props = measure.regionprops(mask, _image)[0];
        # To store the sample points (pixel coordinates + pixel value)
        _datapoints = []
        # To store only the pixel coordinates
        _coords = []

        # turn on interactive mode. Required in VS for displaying figures interactively
        # during script execution
        # plt.ion()

        # Read the file
        with open(_anomalyfile, 'rU') as inp:
            reader = csv.reader(inp)
            for row in reader:
                _datapoints.append([row[1], row[2], row[0]])
                _coords.append([row[1], row[2]])

        # Convert the values from string to integers using this hack I found
        # on Stack Overflow
        _datapoints = map(myFloat, _datapoints)
        _coords = map(myFloat, _coords)
        _coords = map(myInt, _coords)

        # Convert the lists into arrays
        _datapoints = np.asarray(_datapoints)
        _coords = np.asarray(_coords)

        # Normalize the data points (0 mean and 1 standard deviation)
        _center_xform = StandardScaler().fit_transform(_datapoints)

        # Do the clustering
        db = DBSCAN(eps=0.3, min_samples=20).fit(_center_xform)

        labels = db.labels_
        labels_set = set(labels)
        #print labels_set
        # Remove the anomalies label
        labels_set.discard(-1)

        # Non-empty clusters found
        nclusters = 0

        for k in labels_set:
            # Get points in the current cluster
            members = (labels == k)
            members = _coords[members]

            # Form a binary image representing the cluster as points with value 1
            bw = np.zeros((480, 640), dtype=bool)
            for c in members:
                # Array indexing needs a tuple lists don't work
                xy = tuple(c)
                bw[xy] = 1

            # Merge the points into one large region
            bw = morphology.binary_closing(bw, np.ones((3, 3)), iterations=6)
            bw = morphology.binary_opening(bw, np.ones((3, 3)), iterations=3)
            bw = morphology.binary_fill_holes(bw)
            # Remove very small regions
            skimorph.remove_small_objects(bw, in_place=True)

            # Need to do this to avoid error in latest skimage library
            bw = bw.astype(int);

            # Binary image contains a region?
            if bw.any():
                nclusters += 1

                points = bw.nonzero()
                values = _image[points]
                cluster_props = measure.regionprops(bw, _image)[0]

                features = {}

                # These two are not features; they are only used for plotting
                features['points'] = points
                features['values'] = values

                # Eccentricity of the ellipse
                features['eccentricity'] = cluster_props.eccentricity

                # Diameter of the circle with the same area as the region
                # Normalized using image width
                features['eq_diameter'] = cluster_props.equivalent_diameter / 640

                # Number of objects - number of holes (8 connectivity)
                features['euler_number'] = cluster_props.euler_number
                # Fraction of area of entire fruit occupied
                features['area'] = 1. * cluster_props.area / _props.area

                # Ratio of pixels in the region to pixels of the convex hull
                features['solidity'] = cluster_props.solidity

                # Ellipse properties
                features['major_axis'] = 1. * cluster_props.major_axis_length / _props.major_axis_length
                features['minor_axis'] = 1. * cluster_props.minor_axis_length / _props.minor_axis_length

                # Normalized mean pixel value and standard deviation
                features['mean_value'] = 1. * cluster_props.mean_intensity / _props.max_intensity
                features['std'] = np.std(values) / _props.max_intensity

                hist = values.copy()
                hist = hist - _props.min_intensity
                hist = 256. * hist / _props.max_intensity
                hist = hist.astype(int)
                bins = np.bincount(hist, minlength=256)
                hist = []
                for i in range(0, 32):
                    start = i * 4
                    end = start + 4
                    v = 1. * sum(bins[start:end]) / values.size
                    hist.append(v)
                    features['hist' + str(i)] = v

                plt.figure()
                plt.bar(np.arange(32), hist)
                #plt.savefig(prefix + postfix + "_Histogram_" + str(nclusters) + ".png")
                print("->->->->->", _junk + file_name + postfix)
                plt.savefig(_junk + file_name + "_" + postfix + "_Histogram_" + str(nclusters) + ".png")
                _feature_data.append(features)

            plt.close()
    # for cluster in _feature_data:
    #    points = cluster['points']
    #    im = np.zeros((480, 640), dtype=int)
    #    im[points] = cluster['values']
    #    plt.figure()
    #    plt.imshow(im, cmap='gray')

    # plt.show()
    n1 = csvwrite(_imagefile, _feature_data, permanent_dir)
    # n2 = csvwrite_histo(_imagefile, _hist_data);
    # mergeCSV(n1, n2);
    return _feature_data


def csvwrite(_imagefile, _feature_data, write_dir):
    print("Writing FEATURE.CSV file...")
    feature_file = os.path.splitext(_imagefile)[0]
    feature_file = feature_file.replace("IR", "Features")

    name = feature_file + '.csv';
    with open(name, 'w') as csvfile:
        fieldnames = ['mean_value', 'euler_number', 'major_axis', 'area', 'solidity', 'std', 'eccentricity',
                      'eq_diameter', 'minor_axis']
        fieldnames.extend(getHistFeatureKeys())

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames);
        writer.writeheader()

        for cluster in _feature_data:
            data = {key:value for key, value in cluster.items() if key in fieldnames}
            writer.writerow(data)
    print write_dir
    
    os.rename(name, write_dir + "\\" + "output.csv")
    #copy2(outpu, _junk)
    #os.rename(_junk, "output.csv")
    print("FEATURE.CSV file is Written")

if __name__ == '__main__':
    takeInput();
