

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



pip install plotly

import plotly.express as px

data = pd.read_csv('Ue.csv')
#load our data set using pandas

data.info()

data.head()

data.tail()

data.describe()

data.isna().sum()

data.corr()



fig = px.line(data, x=' Date', y=' Estimated Unemployment Rate (%)', color='Region', title='Unemployment Rate Over Time')
fig.show()



fig = px.scatter(data, x=' Estimated Employed', y=' Estimated Unemployment Rate (%)', color='Region', title='Employment vs. Unemployment Rate')
fig.show()

fig = px.bar(data, x='Region', y=' Estimated Employed', title='Employed Population by Region')
fig.show()
plt.tight_layout()

pip install dash

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

#Create a Dash web application:
app = dash.Dash(__name__)

#define layout of our dashboard
app.layout = html.Div([
    dcc.Graph(id='unemployment-graph'),
    dcc.Dropdown(
        id='region-dropdown',
        options=[
            {'label': region, 'value': region}
            for region in data['Region'].unique()
        ],
        value='Andhra Pradesh'  # Set an initial region
    )
])

#Define callback functions to update the graph based on user input:
@app.callback(
    Output('unemployment-graph', 'figure'),
    [Input('region-dropdown', 'value')]
)
def update_graph(selected_region):
    filtered_data = df[df['Region'] == selected_region]

    fig = px.line(
        filtered_data,
        x='Date',
        y='Estimated Unemployment Rate (%)',
        title=f'Unemployment Rate Over Time in {selected_region}',
    )

    return fig

#Run the Dash application:
if __name__ == '__main__':
    app.run_server(debug=True)

pip install plotly geopandas geoplot

import geopandas as gpd
import geoplot as gplt
import geoplot.crs as gcrs
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

