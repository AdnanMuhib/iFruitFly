####################################################################
##########################-Header File-############################# 
####################################################################

#Built in libraries
from shutil import copy2
from time import gmtime, strftime
import subprocess
import os
import re
import fnmatch
import sys
import shutil
import csv


#ifruitfly detector libraries
import imageSegmentor_v3 as segmentor
import cluster_analysis_feature_extraction as iFruitFly_clustering
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn import preprocessing
import matplotlib.pyplot as plt
from math import sqrt

#other helping libraries
import matplotlib.pyplot as plt
from scipy import misc
import numpy as np
import csv

####################################################################
###########################-MAIN FILE-##############################
####################################################################

def python_wrapper(mImage, prefix, file_name, pre_prefix, dir, permanent_dir):    
    # tokenization of images
    token = re.split('RGB_|.png', mImage)
    ir_directory = token[0] + 'IR_' + token[1] + '.pgm'
    mat_directory = token[0] + 'Mat_' + token[1]
    
    # get mat and ir image
    image = segmentor.getImage(ir_directory)
    mat = segmentor.readMatFile(mat_directory)

    # image processing
    edges = segmentor.edgeDetector(image)
    type = segmentor.getTypeOfFruit(image)
    segmentation = segmentor.segmentation(image, type)
    filter = segmentor.filterImageFromSegmentation(image, segmentation)
    output_seg = segmentor.imageMapping(filter, mat['IR'])

    ####################-Anomaly Detection via INFLO-###################

    # file prefix creation for the csv file to save
    prefix_csv = prefix + file_name

    # if folder is not there then create it
    # and right the csv to the folder
    if not os.path.exists(prefix):
       os.mkdir(prefix)
       csv = segmentor.writeToCSV(output_seg, prefix_csv)
       print "file is written"

    #else simply write the csv to the folder
    else:
       csv = segmentor.writeToCSV(output_seg, prefix_csv)
       print "file is written"
    #call the INFLO.bat after segmenting the image
    #for anomaly detection
    run_batch_file("rapid_miner_pro_ifruitlfy.bat")
    ############################-Clustering-############################
 
    # image file directory is stored in ir_directory
    # mat file directory is stored in mat_directory
    # and need to get the INFLO file
    # directory for INFLO file is prefix_csv
    anomaly_file = prefix_csv + '.csv_INFLO.csv' 
    # directory for the temperorary files is made so
    # some results can be stored and processed auto-
    # matically by the rapid miner 5, this folder is
    
    demo_printing_picture(permanent_dir, prefix, mImage, pre_prefix, dir)
    print("END OF ANOMALY DETECTION CLICK TRAIN AND SHOW RESULT FOR PROCESSING")
    write_temp_dir = permanent_dir + "\\"
    print prefix
    print file_name
    features = iFruitFly_clustering.cluster_analysis.cluster_analysis(ir_directory,
                                                                  permanent_dir + "\\output_INFLO.csv", 
                                                                  mat_directory, 
                                                                  dir + "\\" + file_name, 
                                                                  prefix, file_name, 
                                                                  permanent_dir)
    if (features == None):
        print("Image cant be segmented due to poor calibiration")

    #other files are stored for the user in the junk
    else:
        print "printing images->>>>>>> ", prefix + file_name
        image_plotter(features, ir_directory, prefix + file_name)
    #calling rapid miner for further training
    run_batch_file("rapid_miner_pro_train_c#.bat")
    ##############################-END-#################################
    return
    
def demo_printing_picture(anomaly_file, prefix, rgb_directory, pre_prefix, dir):
    #clusters = webDemo.main(anomaly_file,
    #"D:\\ifruitly_junk\\results\\result.jpg")
    clusters = v_demo(anomaly_file, prefix, pre_prefix, file_name, dir)
    return

############################################################################

def myFloat(myList):
    return map(float, myList)

def myInt(myList):
    return map(int, myList)

def myTemp(myList):
    return map(int, myList)

def v_demo(dir, prefix, pre_prefix, file_name, _dir):
    _val = []
    _coords = []
    file_dir_fix = dir + "\\output_INFLO.csv"
    #f = "C:\Users\Abdullah Akmal\Documents\ifruitfly_temp\output_files\output_INFLO.csv"
    with open(file_dir_fix, 'rU') as inp:
        rd = csv.reader(inp)
        for row in rd:
            _val.append([row[1], row[2], row[0]])
    
    #print(_center)
    _val = np.asarray(_val)
    _val_original = _val
    _val_original = map(myFloat, _val_original)
    _val_original = map(myInt, _val_original)
    #_val_original = map(myTemp, _val_original)
    _val_original = np.asarray(_val_original)
    _val = preprocessing.StandardScaler().fit_transform(_val)
    #_center = preprocessing.MinMaxScaler()
    #_center.fit_transform(_val)
    #_arr = StandardScaler().inverse_transform(_center)
    #print(_arr)
    #print(_center)
    new_file = prefix + file_name + ".png"
    dbFun(_val, _val_original, new_file)
    #_len = len(_center)
    return

def dbFun( _x,_original_vals, f):
    db = DBSCAN(eps=0.3, min_samples=20).fit(_x)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True

    labels = db.labels_
    #print(labels)
    n_clusters_ = len(set(labels)) - (1 if -1 else 0)
    #gettingCharacteristics(_x, core_samples_mask, labels, n_clusters_,
    #_original_vals)
    print("Wait plotting clusters.....")
    plotCluster(_x, labels, core_samples_mask, n_clusters_, f)
    return


def plotCluster( _x, labels, core_samples_mask, n_clusters_, f):
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = 'k'

        class_member_mask = (labels == k)

        xy = _x[class_member_mask & ~core_samples_mask]
        ax = plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                    markeredgecolor='k', markersize=6)

        xy = _x[class_member_mask & core_samples_mask]
        ax = plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                    markeredgecolor='k', markersize=14)
        
    #plt.title('Estimated number of clusters: %d' % n_clusters_)
    #plt.axis('off')
    
    #misc.imrotate(ax, 270)
    index = f
    print f
    plt.axis('off')
    plt.savefig(f)
    image_rotate(f)
    plt.close()
    #plt.show()
    return

def image_rotate( index):
    from PIL import Image
    src = Image.open(index)
    angle = 270
    img = src.rotate(angle)
    img.save(index)

def image_plotter(features_data, image, write_dir):
        fig = plt.figure()
        fig.add_subplot(1, 2, 1)
        fig = plt.figure()
        fig.add_subplot(1, 2, 1)
        print("Processing Please Wait...")
        im = misc.imread(image)
        plt.imshow(im)
        n = 1
        for cluster in features_data:
            points = cluster['points']
            im = np.zeros((480, 640), dtype=int)
            im[points] = cluster['values']
            #plt.figure()
            #plt.imshow(im, cmap='gray')
            print("Writing Images...")
            fig.add_subplot(1, 2, 2)
            plt.imshow(im)
            #prefix = re.split('IR_|.pgm', _im)[0]
            #print(prefix)
            #postfix = re.split('IR_|.pgm', _im)[1] 
            #print(postfix)
            plt.axis('off')
            plt.savefig(write_dir + "_Cluster_" + str(n) + ".png")
            n = n + 1
            print("Done..")
        plt.close()
        return

############################################################################
def run_batch_file(file_path):
    #change the directory to the main
    #directory of rapid miner
    os.chdir("C:\Program Files (x86)\Rapid-I\RapidMiner5\scripts")
    #run the subprocess of the *.bat file
    #and show the log of the current on
    #going processes
    run_proc = subprocess.Popen(file_path,
                                  shell=True,
                                  stdout=subprocess.PIPE)
    #display any error or output to the
    #main console
    stdout, stderr = run_proc.communicate()
    #return with the return code "like -1
    #if there is any error"
    return run_proc.returncode


if __name__ == "__main__":
   
    ###############################################################################
    #arguments from the c#
    mImage = sys.argv[1]
    prefix = sys.argv[2]
    file_name = sys.argv[3]
    dir = sys.argv[4]
    permanent_dir = sys.argv[5]
    pre_prefix = dir
    prefix = prefix + "\\"
    dir = dir + "\\"
    ###############################################################################
   
    ###############################################################################
    #testing
    #F = open('C:\\Users\\Rizwan-AIRL\\Documents\\ifruitfly_temp\\FILE_11.TXT', 'w')
    #F.write(mImage)
    #F.write("\n")
    #F.write(pre_prefix)
    #F.write("\n")
    #F.write(prefix)
    #F.write("\n")
    #F.write(file_name)
    #F.write("\n")
    #F.write(dir)
    ###############################################################################

    #mImage = "C:\\Users\\Rizwan-AIRL\\Desktop\\Python Scripts\\Pictures_Day_1\\Galia_Case_A\\Galia_A_17.08.15_1200_RGB_1.png"
    #prefix = "C:\\Users\\Rizwan-AIRL\\Documents\\ifruitfly_temp\\temp_2017-05-16_02-20-21\\"
    #pre_prefix = "C:\\Users\\Rizwan-AIRL\\Documents\\ifruitfly_temp"
    #file_name = "Galia_A_17.08.15_1200_RGB_1.png"
    #permanent_dir = "C:\\ifruitfly_junk"
    #dir = "C:\\Users\\Rizwan-AIRL\\Documents\\ifruitfly_temp\\"
    ###############################################################################

    ###############################################################################
    #calling the main function
    python_wrapper(mImage, prefix, file_name, pre_prefix, dir, permanent_dir)    
    ###############################################################################