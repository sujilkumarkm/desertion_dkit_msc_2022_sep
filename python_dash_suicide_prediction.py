#import packages to create app
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

from gapminder import gapminder

import plotly.express as px
import pandas as pd
import numpy as np

loc_data = pd.read_csv("E:\\Dessertation\\desertion_dkit_msc_2022_sep\\cleaned.csv")
loc_data.tail()

#get unique continents
cont_names = loc_data['continent'].unique()
cols=list(loc_data.columns)
#data for the region plot
# loc_data = px.data.gapminder()

# Create the dash app
app = dash.Dash(__name__)
#change background and color text
colors = {
    #background to rgb(233, 238, 245)
    'background': '#0066cc',
    'text': '#ffffff'
}


fig= px.choropleth(loc_data,locations="country", color="suicides",
hover_name="country",hover_data=['continent','population'],animation_frame="year",    
color_continuous_scale='Turbo',range_color=[28, 92],
labels={'population':'Population','year':'Year','continent':'Continent',
    'country':'Country','suicides':'Life Expectancy'})
fig.update_layout(plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)')





app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1('Gapminder',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    #Add multiple line text 
    html.Div('''
        Life Expectancy vs GDP per Capita for different Countries from 1952 to 2007 
    ''', style={
        'textAlign': 'center',
        'color': colors['text']}
    ),

    html.Label('Select Continent/Continents'),
    dcc.Dropdown(id='cont_dropdown',
                 options=[{'label': i, 'value': i}
                          for i in cont_names],
                 value=['Asia','Europe','Africa','Americas','Oceania'],
                 multi=True,
                style={'width':'70%'}
    ),

    dcc.Graph(
        id='suicidesVsGDP'
    ),
    html.Div([
        html.Div([
            dcc.Graph(
                id='suicides',
                figure=fig
            )
        ],style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(
                id='suicidesOverTime',
            )
        ],style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    ])

])

@app.callback(
    [Output(component_id='suicidesVsGDP', component_property='figure'),
    Output(component_id='suicidesOverTime', component_property='figure')],
    Input(component_id='cont_dropdown', component_property='value')
)
def update_graph(selected_cont):
    if not selected_cont:
        return dash.no_update
    data =[]
    for j in selected_cont:
            data.append(gapminder[gapminder['continent'] == j])
    df = pd.DataFrame(np.concatenate(data), columns=cols)
    df=df.infer_objects()
    scat_fig = px.scatter(data_frame=df, x="gdpPercap", y="suicides",
                size="population", color="continent",hover_name="country", 
               #add frame by year to create animation grouped by country
               animation_frame="year",animation_group="country",
               #specify formating of markers and axes
               log_x = True, size_max=60, range_x=[100,100000], range_y=[28,92],
                # change labels
                labels={'population':'Population','year':'Year','continent':'Continent',
                        'country':'Country','suicides':'Life Expectancy','gdpPercap':"GDP/Capita"})
    # Change the axis titles and add background colour using rgb syntax
    scat_fig.update_layout({'xaxis': {'title': {'text': 'log(GDP Per Capita)'}},
                  'yaxis': {'title': {'text': 'Life Expectancy'}}}, 
                  plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)')
    line_fig = px.line(data_frame=df, 
                x="year",  y="suicides", color='continent',line_group="country", 
                hover_data=['population','year'],
                 # Add bold variable in hover information
                  hover_name='country',
                 # change labels
                 labels={'ulation':'Population','year':'Year','continent':'Continent',
                     'country':'Country','suicides':'Life Expectancy'})
    line_fig.update_layout(plot_bgcolor='rgb(233, 238, 245)',
        paper_bgcolor='rgb(233, 238, 245)')
    return [scat_fig, line_fig]



if __name__ == '__main__':
    app.run_server(port=80,debug=True)
