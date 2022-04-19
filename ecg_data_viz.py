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
from sklearn import preprocessing
from util import *

####################################################################################
# Initial Data Visvulization for ECG data.                                         #
# Powered by Plotly Dash                                                           #
####################################################################################

app = dash.Dash(__name__)
# list all files ending with a .txt.
all_files_txt = glob.glob("/Users/shehjarsadhu/Desktop/HardwareSecurityFinal/CYBHi/data/short-term/*txt")

only_file_name_8B, only_file_name_85 = file_paths_query(all_files_txt)

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
    
    # Calulate FFT for Raw ECG
    xf, yf, y_det = my_fft(df.iloc[:, 3])
    # Normalized ECG.
    normalized_arr_ecg = preprocessing.normalize([df.iloc[:, 3]])
    # FFT for Normalized ECG.
    xf_norm, yf_norm, y_det_norm = my_fft(normalized_arr_ecg[0])

    yf_max_amplitude, xf_freq_max_amt = freq_max_amp(yf,xf)
    yf_norm_max_amplitude, xf_norm_freq_max_amt = freq_max_amp(yf_norm, xf_norm)
    #print("RAW yf_max_amplitude, xf_freq_max_amt: ",yf_max_amplitude,xf_freq_max_amt)
    #print("NORMALIZED yf_norm_max_amplitude, xf_norm_freq_max_amt: ",yf_norm_max_amplitude, xf_norm_freq_max_amt)
    # NOW get the fre and the min amplitudes for normalized and rawe ECG signals.
    yf_min_amplitude, xf_freq_min_amt = freq_min_amp(yf,xf)
    yf_norm_min_amplitude, xf_norm_freq_min_amt = freq_min_amp(yf_norm,xf_norm)
    fig = make_subplots(rows=5, cols=1, vertical_spacing = 0.15,
        subplot_titles=(
            "ECG-3-28 " + ecg_title + "<br>",
            "Raw ECG FFT " + "<br> Max Amplitude: " + str(yf_max_amplitude) + 
            ",Min Amplitude: " + str(yf_min_amplitude) + "\n ,Mean Amplitude: " + str(abs(yf[1:int(len(abs(yf))/2)]).mean())
            + "<br> Freq at Max Amplitude: "+ str(xf_freq_max_amt) + ", Freq at Min Amplitude: " + str(xf_freq_min_amt),
            "Normalized (0-1) ECG <br>",
            "Normalized (0-1) ECG FFT "+
            "<br> Max Amplitude: " + str(yf_norm_max_amplitude) + 
            ",Min Amplitude: " + str(yf_norm_min_amplitude) +
             ",Mean Amplitude: " + str(abs(yf_norm[1:int(len(abs(yf_norm))/2)]).mean())
             + "<br> Freq at Max Amplitude: "+ str(xf_norm_freq_max_amt) + ", Freq at Min Amplitude: " + str(xf_norm_freq_min_amt)
            ))
    fig.add_trace(go.Scatter(y=df.iloc[:, 3], mode='lines',marker_color='teal'),
              1, 1)
    fig.add_trace(go.Scatter(x=xf, y=  abs(yf)[1:int(len(abs(yf))/2)] , mode='lines',marker_color='teal'),
             2, 1)
    fig.add_trace(go.Scatter(y=normalized_arr_ecg[0],  mode='lines',marker_color='teal'),
            3, 1)
    fig.add_trace(go.Scatter(x=xf_norm,y= abs(yf_norm)[1:int(len(abs(yf_norm))/2)],mode='lines',marker_color='teal'),
            4, 1)
    fig.add_trace(go.Box(y= abs(yf_norm)[1:int(len(abs(yf_norm))/2)]),
            5, 1)          

    large_rockwell_template = dict(
    layout=go.Layout(title_font=dict(family="Rockwell")))
    #fig.update_yaxes(title_text="Total Days of Use",title_font_family="IBM Plex San", row=1, col=1)
    fig.update_xaxes(title_text="Number of Samples <br>", title_font_family="IBM Plex San",row=1, col=1)
    fig.update_yaxes(title_text="Amplitude ", title_font_family="IBM Plex San",row=2, col=1)
    fig.update_xaxes(title_text="Frequency in Hz <br>", title_font_family="IBM Plex San",row=2, col=1)
    fig.update_yaxes(title_text="Amplitude", title_font_family="IBM Plex San", row=4, col=1)
    fig.update_xaxes(title_text="Number of Samples <br>", title_font_family="IBM Plex San",row=3, col=1)
    fig.update_xaxes(title_text="Frequency in Hz <br>", title_font_family="IBM Plex San",row=4, col=1)

    fig.update_layout(
        font_family="IBM Plex Sans",
        title= "Check Your Bio Signals (CyBHi) ECG Database Short Term Experiment @Sampling Frequency 1 kHz, N(Palms Only) =" + str(len(only_file_name_8B)) + " N(Finger ECG) =  " + str(len(only_file_name_85)),
        template=large_rockwell_template,height=1000, width=1500) 
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)