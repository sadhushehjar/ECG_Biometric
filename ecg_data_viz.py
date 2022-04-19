import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import json
import dash_bootstrap_components as dbc
import glob
app = dash.Dash(__name__)
# list all files ending with a .txt.
all_files_txt = glob.glob("/Users/shehjarsadhu/Desktop/HardwareSecurityFinal/CYBHi/data/short-term/*txt")

# Takes in a list of file in the shortterm folder.
#Retuns File paths for two devices using based on device ID.
def file_paths_quey(all_files_txt):
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

only_file_name_8B, only_file_name_85 = file_paths_quey(all_files_txt)
#print("fileapth_CI_A1_A2_8B, fileapth_CI_A1_A2_85 ",only_file_name_8B, only_file_name_85)

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                        id='device_id',
                        options=  [{'label': i, 'value': i} for i in ["8B","85"]],
                        placeholder="Select Device ID ",
                        value ="8B"),
            dcc.Dropdown(
                            id='patient_id_filter',
                            options=  [],
                            placeholder="Select Patient ",
                            
                        ),
  
        ],
        style={'width': '48%', 'display': 'inline-block'}),
    ]),
    dcc.Graph(id='indicator-graphic'),
    

])
# Chained callback filer by patient ID and Device ID.
@app.callback(
    Output('patient_id_filter', 'options'),
    Input('device_id', 'value'))
def dates_dropdown(device_id):
    if device_id == "8B":
        return [{'label': i, 'value': i} for i in only_file_name_8B]
    if device_id == "85":
        return [{'label': i, 'value': i} for i in only_file_name_85] 

# For a single channel calculates the FFT of the signal. 
# Returns list of values in freq domain.
def my_fft(y_det):
    # y_det = signal.detrend(X)
    # Number of samples in normalized_tone
    Fs = 1000 # Sampeling rate / # Samples per second.
    Ts = 1/Fs  # Time in seconds between samples.
    N =  len(y_det) 
    xf = np.arange(0, Fs, Fs/N )
    # Pads with 0s automatically if the signal does not match n.
    yf = np.fft.fft(y_det,n=len(xf))# Amptitude. # len 128.
    return xf, yf, y_det

# Displays graphs.
@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('patient_id_filter', 'value'),)
def update_graph(pid):
    print("Patient ID selected",pid)
    df = pd.read_csv("/Users/shehjarsadhu/Desktop/HardwareSecurityFinal/CYBHi/data/short-term/"+pid,sep="\t", skiprows=8,header=None)
    print("pid",pid.split("-"))
    pid_split = pid.split("-")
    # To change the title text of ecg signals.
    if pid_split[3] == "8B.txt":
        ecg_title = "ECG-3-28: Hand Palms (with Ag/Cl electrode and no gel)"
    if pid_split[3] == "85.txt":
        ecg_title = "ECG-3-83 Index and Middle finges (with electrolyca)"
    
    # Calulate ECG
    xf, yf, y_det = my_fft(df.iloc[:, 3])
    #print("yf  ====",yf)
    #yf_list = abs(yf).tolist()
    #print("yf_list======== \n",yf_list)
    #yf_min = yf_list.remove(max(abs(yf)))
    #print( "yf min,\n",yf_min)
    fig = make_subplots(rows=4, cols=1,
        subplot_titles=("1: ECG-3-28 " + ecg_title,"FFT " + str(max(abs(yf))),"3: LDR-1-4 IPAD SCREEN","4:  EDA-1-25 Left Hand"))
    fig.add_trace(go.Scatter(y=df.iloc[:, 3], mode='lines',marker_color='teal'),
              1, 1)
    fig.add_trace(go.Scatter(x=xf, y=  abs(yf) , mode='lines',marker_color='teal'),
             2, 1)
    fig.add_trace(go.Scatter(y=df.iloc[:, 5],  mode='lines',marker_color='teal'),
            3, 1)
    fig.add_trace(go.Scatter(y=df.iloc[:, 4],mode='lines',marker_color='teal'),
            4, 1)       

    large_rockwell_template = dict(
    layout=go.Layout(title_font=dict(family="Rockwell")))
    #fig.update_yaxes(title_text="Total Days of Use",title_font_family="IBM Plex San", row=1, col=1)
    fig.update_xaxes(title_text="Number of Samples", title_font_family="IBM Plex San",row=1, col=1)
    #fig.update_yaxes(title_text="Count of Websites visited", title_font_family="IBM Plex San",row=2, col=1)
    fig.update_xaxes(title_text="Number of Samples", title_font_family="IBM Plex San",row=2, col=1)
    #fig.update_yaxes(title_text="Count of Websites visited",title_font_family="IBM Plex San", row=4, col=1)
    fig.update_xaxes(title_text="Number of Samples", title_font_family="IBM Plex San",row=3, col=1)
    fig.update_xaxes(title_text="", title_font_family="IBM Plex San",row=4, col=1)

    fig.update_layout(
        font_family="IBM Plex Sans",
        title= "Check Your Bio Signals (CyBHi) ECG Database Short Term Experiment @Sampling Frequency 1 kHz",
         template=large_rockwell_template,height=1000, width=1500
         ) 
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)