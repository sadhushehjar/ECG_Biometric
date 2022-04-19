
import pandas as pd
import numpy as np

# Takes in a list of file in the shortterm folder.
#Retuns File paths for two devices using based on device ID Hands and Palm ECG.
def file_paths_query(all_files_txt):
    #CI_A1_A2 => Short Term, A0=>Long Term db
    # file path list for only A1,A2,C1 experiemtns
    fileapth_CI_A1_A2_8B = [] 
    fileapth_CI_A1_A2_85 = []
    only_file_name_8B  = []
    only_file_name_85  = []
    # get filepaths for A1,A2,C1 using split.
    for i in all_files_txt:
        s_path = i.split("/")
        file_name = s_path[8].split("-")
        if file_name[2] == "A2" or file_name[2] == "A1" or file_name[2] == "CI":
            # print("Only for A1,A2,C1 experiemtns \n,",i)
            #print("s_path[8]:,", s_path[8], file_name[3])
            # Check the device ID columns are based on device ID.
            if file_name[3] == "8B.txt":
             #   print("s_path[8]: 8B",s_path[8])
                fileapth_CI_A1_A2_8B.append(i)
                only_file_name_8B.append(s_path[8])
            if file_name[3]  == "85.txt":
              #  print("s_path[8] 85",s_path[8])
                only_file_name_85.append(s_path[8])
                fileapth_CI_A1_A2_85.append(s_path[8])
    return only_file_name_8B, only_file_name_85

# For a single channel calculates the FFT of the signal. 
# Returns list of values in freq domain.
def my_fft(y_det):
    # y_det = signal.detrend(X)
    # Number of samples in normalized_tone
    Fs = 1000 # Sampling rate / # Samples per second.
    Ts = 1/Fs  # Time in seconds between samples.
    N =  len(y_det) 
    xf = np.arange(0, Fs, Fs/N )
    # Pads with 0s automatically if the signal does not match n.
    yf = np.fft.fft(y_det,n=len(xf))# Amptitude. # len 128.
    return xf, yf, y_det
# Returns Frequency of Max Amplitude and Max Amplitude.
def freq_max_amp(yf,xf):
    yf_half_no_dc = yf[1:int(len(abs(yf))/2)]
    yf_max_amplitude = max(yf_half_no_dc)
    yf_max_index = np.where(yf_half_no_dc == yf_max_amplitude)
    xf_freq_max_amt = xf[yf_max_index] # x value i.e freq in Hz for the max amplitude.
    return yf_max_amplitude, xf_freq_max_amt

# Returns Frequency of Min Amplitude and Min Amplitude.
def freq_min_amp(yf,xf):
    yf_half_no_dc = yf[1:int(len(abs(yf))/2)] # Remove DC component and half of the FTT 
    yf_min_amplitude = min(yf_half_no_dc)
    yf_min_index = np.where(yf_half_no_dc == yf_min_amplitude) # Get the index of the min amplidude
    xf_freq_min_amt = xf[yf_min_index] # x value i.e freq in Hz for the max amplitude.
    return yf_min_amplitude, xf_freq_min_amt 
