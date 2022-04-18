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
fileapth_CI_A1_A2 = [] # file path list for only A1,A2,C1 experiemtns
only_file_name  = []
# get filepaths for A1,A2,C1 using split.
for i in all_files_txt:
    s_path = i.split("/")
    file_name = s_path[8].split("-")
    if file_name[2] == "A2" or file_name[2] == "A1" or file_name[2] == "CI":
        #print("Only for A1,A2,C1 experiemtns \n,",i)
        fileapth_CI_A1_A2.append(i)
        only_file_name.append(s_path[8])

 #df = pd.read_csv("/Users/shehjarsadhu/Desktop/HardwareSecurityFinal/CYBHi/data/short-term/20110718-ARS-A2-8B.txt",sep="\t", skiprows=8)

app.layout = html.Div([
    html.Div([
        html.Div([
 dcc.Dropdown(
                id='patient_id_filter',
                options=  [{'label': i, 'value': i} for i in only_file_name],
                placeholder="Select Patient ",
                value =only_file_name[0]
            ),
        ],
        style={'width': '48%', 'display': 'inline-block'}),
    ]),
    dcc.Graph(id='indicator-graphic'),
    

])
# Displays graphs.
@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('patient_id_filter', 'value'),)
def update_graph(pid):
    print("Patient ID selected",pid)
    df = pd.read_csv("/Users/shehjarsadhu/Desktop/HardwareSecurityFinal/CYBHi/data/short-term/"+pid,sep="\t", skiprows=8,header=None)
    print("df columns",df.columns)
    print("Column y = \n",df.iloc[:, 3])
    print("Column x = \n",df.iloc[:, 0])
    fig = make_subplots(rows=4, cols=1,
        subplot_titles=("1: ECG-3-28 , Hand palms (with Ag/Cl electrode and no gel) ","2:EDA-1-25 Left Hand ","3: LDR-1-4 IPAD SCREEN","4: LDR-1-7 LED"))
    fig.add_trace(go.Scatter(y=df.iloc[:, 3], mode='lines',marker_color='teal'),
              1, 1)
    fig.add_trace(go.Scatter(y=df.iloc[:, 4],mode='lines',marker_color='teal'),
             2, 1)
    fig.add_trace(go.Scatter(y=df.iloc[:, 5],  mode='lines',marker_color='teal'),
            3, 1)
    fig.add_trace(go.Scatter(y=df.iloc[:, 6] ,mode='lines',marker_color='teal'),
            4, 1)       

    large_rockwell_template = dict(
    layout=go.Layout(title_font=dict(family="Rockwell")))
    #fig.update_yaxes(title_text="Total Days of Use",title_font_family="IBM Plex San", row=1, col=1)
    #fig.update_xaxes(title_text="Paticipant ID", title_font_family="IBM Plex San",row=1, col=1)
    #fig.update_yaxes(title_text="Count of Websites visited", title_font_family="IBM Plex San",row=2, col=1)
    #fig.update_xaxes(title_text="Visited Websites", title_font_family="IBM Plex San",row=2, col=1)
    #fig.update_yaxes(title_text="Count of Websites visited",title_font_family="IBM Plex San", row=4, col=1)
    #fig.update_xaxes(title_text="Visited Websites", title_font_family="IBM Plex San",row=4, col=1)

    fig.update_layout(
        font_family="IBM Plex Sans",
        title= "Check Your Bio Signals ECG Database Short Term Experiment",
         template=large_rockwell_template,height=1000, width=1500
         ) 
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)