import pandas as pd
import numpy as np
import plotly.graph_objects as go
import json
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import re
from dash.dependencies import Input, Output

from config import data_dir

ads_link = os.path.join(data_dir, "google-political-ads-advertiser-weekly-spend.csv")
weekly_spend = pd.read_csv(ads_link)

#Keep columns we want
weekly_spend_usd = weekly_spend[['Advertiser_Name', 'Week_Start_Date', 'Spend_USD', 'Election_Cycle']]
weekly_spend_usd['Week_Start_Date'] = pd.to_datetime(weekly_spend_usd['Week_Start_Date'])

#Keep rows that contain presidents
weekly_spend_usd['Advertiser_Name'] = weekly_spend_usd['Advertiser_Name'].apply(str.lower)

# pres_list = weekly_spend_usd[weekly_spend_usd['Advertiser_Name'].str.contains("bloomberg|\
#                                                 trump|biden|bennet|buttigieg|delaney|gabbard|klobuchar|patrick|sanders|steyer|\
#                                                 warren|yang|walsh|weld")]

bloomberg = weekly_spend_usd[weekly_spend_usd['Advertiser_Name'].str.contains("bloomberg")]
trump = weekly_spend_usd[weekly_spend_usd['Advertiser_Name'].str.contains("trump")]
biden = weekly_spend_usd[weekly_spend_usd['Advertiser_Name'].str.contains("biden")]
bennet = weekly_spend_usd[weekly_spend_usd['Advertiser_Name'].str.contains("bennet")]
buttigieg = weekly_spend_usd[weekly_spend_usd['Advertiser_Name'].str.contains("buttigieg|pete")]
delaney = weekly_spend_usd[weekly_spend_usd['Advertiser_Name'].str.contains("delaney")]
gabbard = weekly_spend_usd[weekly_spend_usd['Advertiser_Name'].str.contains("gabbard|tulsi")]
klobuchar = weekly_spend_usd[weekly_spend_usd['Advertiser_Name'].str.contains("klobuchar")]
warren = weekly_spend_usd[weekly_spend_usd['Advertiser_Name'].str.contains("warren")]
yang = weekly_spend_usd[weekly_spend_usd['Advertiser_Name'].str.contains("yang")]
walsh = weekly_spend_usd[weekly_spend_usd['Advertiser_Name'].str.contains("walsh")]
weld = weekly_spend_usd[weekly_spend_usd['Advertiser_Name'].str.contains("weld")]
sanders = weekly_spend_usd[weekly_spend_usd['Advertiser_Name'].str.contains("sanders|bernie")]
patrick = weekly_spend_usd[weekly_spend_usd['Advertiser_Name'].str.contains("patrick")]
steyer = weekly_spend_usd[weekly_spend_usd['Advertiser_Name'].str.contains("steyer")]

c_d = {
    'Michael Bloomberg' : bloomberg,
    'Donald Trump' : trump,
    'Joe Biden' : biden,
    'Michael Bennet' : bennet,
    'Pete Buttigieg' : buttigieg,
    'John Delaney' : delaney,
    'Tulsi Gabbard' : gabbard,
    'Amy Klobuchar' : klobuchar,
    'Elizabeth Warren' : warren,
    'Andrew Yang' : yang,
    'Joe Walsh' : walsh,
    'William Weld' : weld,
    'Bernie Sanders' : sanders,
    'Deval Patrick' : patrick,
    'Tom Steyer' : steyer
}

drop_down_options = [{'label' : person, 'value' : person}
                     for person in c_d.keys()]

def aggregate_rows(df):
    aggregation_functions = {'Spend_USD':'sum'}
    df_new = df.groupby(df['Week_Start_Date'], as_index=False).aggregate(aggregation_functions)
    return df_new

for key in c_d:
    c_d[key] = aggregate_rows(c_d[key])

def update_fig(df_str):
    data = go.Scatter(
        x=df_str['Week_Start_Date'],
        y=df_str['Spend_USD']
    )
    layout = go.Layout(
        # yaxis_range=[0, 4],
        xaxis_range=['2018-12-01','2020-01-05'],
        template = 'plotly_dark',
        yaxis={
            'type':'log'
        }
    )
    fig = go.Figure(data=data, layout=layout)
    return fig

app = dash.Dash()
app.layout = html.Div(children=[
    dcc.Dropdown(
        id='candidate_drop',
        options=drop_down_options,
        value='Michael Bloomberg'
    ),
    dcc.Graph(
        id = 'spent_series_chart',
        figure=update_fig(c_d['Michael Bloomberg']), #should return dataframe
        config = {
            'displayModeBar' : False,
            'editable':False,
        }
    )
])

@app.callback(
    Output('spent_series_chart', 'figure'),
    [Input(component_id='candidate_drop', component_property='value')]
)

def update(input_val):
    return update_fig(c_d[input_val])

if __name__ == '__main__':
    app.run_server(debug=False)