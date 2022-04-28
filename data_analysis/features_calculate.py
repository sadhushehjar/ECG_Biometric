import glob
import pandas as pd
import numpy as np
from sklearn import preprocessing
import time
from util import *

#### FEATURE TABLE EXAMPLE
###########################################
# AmtMax, AmtMin, AmtMean, UniqueID
#           
###########################################
#### TIMMING EXPERIMET EXAMPLE
###########################################
# NormTS, fftTS,AmtMaxTS, AmtMinTS, AmtMeanTS, UniqueID

###########################################

# Input - Raw normalized (0-1) ECG signal.
# Output above mentioned feature table.
def calculate_features():
    # Read all participants data.
    # list all files ending with a .txt.
    root = "/Users/shehjarsadhu/Desktop/HardwareSecurityFinal/CYBHi/data/short-term/"
    all_files_txt = glob.glob("/Users/shehjarsadhu/Desktop/HardwareSecurityFinal/CYBHi/data/short-term/*txt")
    # Query filepaths based on device ID which determins wether the sensor is placed on hand or palm.
    only_file_name_8B, only_file_name_85 = file_paths_query(all_files_txt)
    ## Create list to create the feature dataframe.
    uniqueID = []
    max_amt = []
    min_amt = []
    mean_amt = []
    # For timming results 
    NormTS = []
    fftTS = []
    AmtMaxTS =[] 
    AmtMinTS = [] 
    AmtMeanTS = []
    # 8B IS FOR HANDS ONLY.
    for filename in only_file_name_8B: 
        print("Calculating features for ==== " ,filename)
        #print("Device ID 8B filenames:",filename)
        df = pd.read_csv(root + filename,sep="\t", skiprows=8,header=None)
        # # For each participant ------- 
        # 1. Normalize features.
        # print("RAW ECG-------- ",df.iloc[:, 3])
        start_time_norm = time.time()
        normalized_arr_ecg = preprocessing.normalize([df.iloc[:, 3]]) # 3 is the column for ECG data.
        end_time_norm = time.time()
        NormTS.append(str(end_time_norm-start_time_norm))
        
        # 2. Calcualte FFT features for Normalized ECG.
        start_time_fft = time.time()
        xf_norm, yf_norm, y_det_norm = my_fft(normalized_arr_ecg[0])
        end_time_fft = time.time()
        fftTS.append(str(end_time_fft-start_time_fft))
        
        start_time_max_fft = time.time()
        yf_norm_max_amplitude, xf_norm_freq_max_amt = freq_max_amp(yf_norm, xf_norm)
        print(yf_norm_max_amplitude,"\n",type(yf_norm_max_amplitude))
        end_time_max_fft = time.time()
        AmtMaxTS.append(str(end_time_max_fft-start_time_max_fft))
        start_time_min_fft = time.time()
        yf_norm_min_amplitude, xf_norm_freq_min_amt = freq_min_amp(yf_norm,xf_norm)
        end_time_min_fft = time.time()
        #AmtMaxTS, AmtMinTS, AmtMeanTS,
        AmtMinTS.append(str(end_time_min_fft-start_time_min_fft))
        start_time_mean_fft = time.time()
        yf_norm_mean_amplitude = yf_norm[1:int(len(abs(yf_norm))/2)].mean()
        end_time_mean_fft = time.time()
        AmtMeanTS.append(str(end_time_mean_fft-start_time_mean_fft))
        max_amt.append(yf_norm_max_amplitude)
        min_amt.append(yf_norm_min_amplitude)
        mean_amt.append(abs(yf_norm_mean_amplitude))
        uniqueID.append(filename)
        
    print("len(max_amt),len(min_amt),len(mean_amt),len(uniqueID)= ",len(max_amt),len(min_amt),len(mean_amt),len(uniqueID))
    features_df = pd.DataFrame({
        "max_amt":max_amt,
        "min_amt": min_amt,
        "mean_amt":mean_amt,
        "uniqueID":uniqueID
    })
    features_df_timing = pd.DataFrame({
            "NormTS" : NormTS,
            "fftTS" : fftTS,
            "AmtMaxTS" :AmtMaxTS,
            "AmtMinTS" :AmtMinTS,
            "AmtMeanTS" : AmtMeanTS,
            "uniqueID":uniqueID
    })
    #features_df.to_csv("/Users/shehjarsadhu/Desktop/HardwareSecurityFinal/ECG_feature_tables/features_freq.csv",index=0)
    #features_df_timing.to_csv("/Users/shehjarsadhu/Desktop/HardwareSecurityFinal/ECG_feature_tables/features_freq_timming.csv",index=0)
if __name__ == '__main__':
    calculate_features()