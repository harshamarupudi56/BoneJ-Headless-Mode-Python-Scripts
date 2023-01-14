6#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 17:03:31 2022

@author: sriharsha.marupudi
"""

import numpy as np
import nrrd
import csv 
import os
import subprocess 
from glob import glob
import tempfile 
import sys 
import matplotlib.pyplot as plt 

from contextlib import contextmanager
import sys, os


# BoneJ Function wrapper
# def BoneJ(array,voxel_size,Fiji_path):
    
# Define function for each individual plugin 
#Require installation of Fiji with BoneJ plugins

NAME = "1_04216"
array,array1header = nrrd.read(f"/gpfs_projects/sriharsha.marupudi/Segmentations_Otsu_L1/Segmentation-grayscale-{NAME}.nrrd")  # should be a numpy array
voxel_size = [51.29980, 51.29980, 51.29980] #microns 
fiji_path = "~/Fiji.app/ImageJ-linux64"

  

# feed in numpy array

nLines_list = [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384]
NDirs_list = [16,32,64,128,256,512,1024,2048,4096,8192]
csv_dir = "/gpfs_projects/sriharsha.marupudi/Anisotropy_Convergence_Test.csv" #location of csv file storing anisotropy convergence measurements 

         
def Anisotropy(array,voxel_size,fiji_path,NDirs = NDirs_list, nLines =nLines_list, samplingincrement = 1.73, radii = False, eigens = False):
    
  
    
    for i in NDirs_list:
        
       
        
       for c in nLines_list:
           


            NDirs = str(i)
            nLines = str(c)
            samplingincrement = str(samplingincrement)
            radii = str(radii)
            eigens = str(eigens)
               
            
            
            tempdir = tempfile.TemporaryDirectory()
            data1_nrrd = os.path.join(tempdir.name, "img.nrrd")
            table_csv = os.path.join(tempdir.name,"table.csv")
            outputdir = os.path.join(tempdir.name, "outputdir")
            macro_file = os.path.abspath("Anisotropy_API_Test.py")
            csv_Dir  = csv_dir
            # save to temporary directory
            header = {'units': ['um', 'um', 'um'],'spacings': voxel_size}
            
            nrrd.write(data1_nrrd,array,header)
            
            # run BoneJ thickness wraapper 
            # table is results of thickness plugin as csv file 
            # thickness_tif is numpy array of thickness images 
            
            fiji_cmd = "".join([fiji_path, " --ij2", " --headless", " --run", " "+macro_file, 
                             " \'image="+"\""+data1_nrrd+"\"",
                             ", NAME="+"\""+NAME+"\"",", NDirs="+"\""+NDirs+"\"",
                             ", nLines="+"\""+nLines+"\"",
                             ", samplingincrement="+"\""+samplingincrement+"\"",
                             ", radii="+"\""+radii+"\"",
                             ", eigens="+"\""+eigens+"\"",
                             ", outputdir="+"\""+outputdir+"\"",
                             ", table_csv="+"\""+table_csv+"\""+"\'"])
            
            b = subprocess.call(fiji_cmd, shell=True)
            with open(outputdir+f"ROI-{NAME}-table.csv", "r",encoding='utf-8') as file:
                reader = csv.reader(file)
                metric_dict = {row[0]:row[1:] for row in reader if row and row[0]}
                print(metric_dict)
                writer = csv.writer(csv_dir,dialect='excel')
                writer.writeheader()
                writer.writerows(metric_dict)
        

    return metric_dict


nVectors_list = [100,200,300,400]
VectorIncrement_list = [1,2,3]
skipRatio_list = [1,2,3]
contactSensitivity_list = [1,2,3]
maxDrift_list = [1,2,3]
maxIterations_list = [30,40,50]
distanceThreshold_list = [.2,.4,.6,.8,1.0]

def Ellipsoid_Factor (array,voxel_size,fiji_path,nVectors = nVectors_list,
vectorIncrement = VectorIncrement_list,
skipRatio = skipRatio_list,
contactSensitivity = contactSensitivity_list,
maxDrift = maxDrift_list,
maxIterations = maxIterations_list,
distanceThreshold = distanceThreshold_list,
runs = 1,
seedOnDistanceRidge = True,
seedOnTopologyPreserving = True,
showFlinnPlots = False,
showConvergence = False,
showSecondaryImages = False):
    
    for i in nVectors_list:
        for j in VectorIncrement_list: 
            for k in skipRatio_list: 
                for l in  contactSensitivity_list: 
                    for m in maxDrift_list: 
                        for n in maxIterations_list: 
                            for o in distanceThreshold_list: 
                                
                                nVectors = str(i)
                                vectorIncrement = str(j)
                                skipRatio = str(k)
                                contactSensitivity = str(l)
                                maxDrift = str(m)
                                maxIterations = str(n)
                                distanceThreshold = str(o)
                                runs = str(runs)
                                seedOnDistanceRidge = str(seedOnDistanceRidge)
                                seedOnTopologyPreserving = str(seedOnTopologyPreserving)
                                showFlinnPlots = str(showFlinnPlots)
                                showConvergence = str(showConvergence)
                                showSecondaryImages = str(showSecondaryImages)
                               
                                tempdir = tempfile.TemporaryDirectory()
                                data1_nrrd = os.path.join(tempdir.name,"img.nrrd")
                                table_csv = os.path.join(tempdir.name,"table.csv")
                                outputdir = os.path.join(tempdir.name, "outputdir")
                                img_ef_tif = os.path.join(tempdir.name,"img_ef.tif")
                                img_volume_tif = os.path.join(tempdir.name,"img_volume.tif")
                                img_id_tif = os.path.join(tempdir.name,"img_id.tif")
                                img_a_tif = os.path.join(tempdir.name,"img_a.tif")
                                img_c_tif = os.path.join(tempdir.name,"img_c.tif")
                                img_ab_tif = os.path.join(tempdir.name,"img_ab.tif")
                                img_bc_tif = os.path.join(tempdir.name,"img_bc.tif")
                                img_seed_points_tif = os.path.join(tempdir.name,"img_seed_points.tif")
                                img_flinn_peak_plot_tif = os.path.join(tempdir.name,"img_flinn_peak_plot.tif")
                                img_unweighted_flinn_plot_tif = os.path.join(tempdir.name,"img_unweighted_flinn_plot.tif")
                                macro_file = os.path.abspath("Ellipsoid_Factor_API_Test.py")
                            
                                # save to temporary directory
                                header = {'units': ['um', 'um', 'um'],'spacings': voxel_size}
                            
                                nrrd.write(data1_nrrd,array,header)
                                
                                # run BoneJ thickness wraapper 
                                # table is results of thickness plugin as csv file 
                                # thickness_tif is numpy array of thickness images 
                               
                                fiji_cmd = "".join([fiji_path, " --ij2", " --headless", " --run", " "+macro_file, 
                                                     " \'image="+"\""+data1_nrrd+"\"", ", img_ef_tif="+"\""+img_ef_tif+"\"",
                                                     ", img_volume_tif="+"\""+img_volume_tif+"\"",", img_id_tif="+"\""+img_id_tif+"\"",
                                                     ", img_a_tif="+"\""+img_a_tif+"\"",", img_b_tif="+"\""+img_c_tif+"\"",
                                                     ", img_ab_tif="+"\""+img_ab_tif+"\"",", img_bc_tif="+"\""+img_bc_tif+"\"",
                                                     ", img_seed_points_tif="+"\""+img_seed_points_tif+"\"",", img_flinn_peak_plot_tif="+"\""+img_flinn_peak_plot_tif+"\"",
                                                     ", img_unweighted_flinn_plot_tif="+"\""+img_unweighted_flinn_plot_tif+"\"",
                                                     ", nVectors="+"\""+nVectors+"\"",
                                                     ", vectorIncrement="+"\""+vectorIncrement+"\"",
                                                     ", skipRatio="+"\""+skipRatio+"\"",
                                                     ", contactSensitivity="+"\""+contactSensitivity+"\"",
                                                     ", maxIterations="+"\""+maxIterations+"\"",
                                                     ", maxDrift="+"\""+maxDrift+"\"",
                                                     ", runs="+"\""+runs+"\"",
                                                     ", seedOnDistanceRidge="+"\""+seedOnDistanceRidge+"\"",
                                                     ", distanceThreshold="+"\""+distanceThreshold+"\"",
                                                     ", seedOnTopologyPreserving="+"\""+seedOnTopologyPreserving+"\"",
                                                     ", showFlinnPlots="+"\""+showFlinnPlots+"\"",
                                                     ", showConvergence="+"\""+showConvergence+"\"",
                                                     ", showSecondaryImages="+"\""+showSecondaryImages+"\"",
                                                     ", outputdir="+"\""+outputdir+"\"",
                                                     ", NAME="+"\""+NAME+"\"",
                                                     ", table_csv="+"\""+table_csv+"\""+"\'"])
                           
                                print(f"{NAME}")             
                                b = subprocess.call(fiji_cmd, shell=True)
                                with open(outputdir+f"ROI-{NAME}-table.csv", "r",encoding='utf-8') as file:
                                    reader = csv.reader(file)
                                    metric_dict = {row[0]:row[1:] for row in reader if row and row[0]}
                                    print(metric_dict)
                                    
                            
                                return metric_dict       



Anisotropy_result = Anisotropy(array,voxel_size,fiji_path,NDirs = NDirs_list, nLines =nLines_list, samplingincrement = 1.73, radii = False, eigens = False) 
Ellipsoid_Factor_result = Ellipsoid_Factor(array,voxel_size,fiji_path,nVectors = nVectors_list,
vectorIncrement = VectorIncrement_list,
skipRatio = skipRatio_list,
contactSensitivity = contactSensitivity_list,
maxIterations = maxIterations_list,
maxDrift = maxDrift_list,
runs = 1,
seedOnDistanceRidge = True,
distanceThreshold = .8,
seedOnTopologyPreserving = True,
showFlinnPlots = False,
showConvergence = False,
showSecondaryImages = False)