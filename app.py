from datetime import date
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import dash_html_components as html
from dash.dependencies import Input, Output


# load data
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/Xiaohulala/Scientific-Visualization/master/countries.geo.json') as response:
    countries = json.load(response)


df1 = pd.read_csv("https://raw.githubusercontent.com/Xiaohulala/Scientific-Visualization/master/worldometer_coronavirus_summary_data.csv",
                 dtype={"name": str})

df2 = pd.read_csv("https://raw.githubusercontent.com/Xiaohulala/Scientific-Visualization/master/worldometer_coronavirus_daily_data.csv")
all_continents = df2.continent.unique()

df3 = pd.read_csv(
    "https://raw.githubusercontent.com/Xiaohulala/scientific-visualization-final-project/master/worldometer_coronavirus_monthly_data.csv")

app = dash.Dash(__name__)
server = app.server

# Chart 1: Covid-19 Cases Per Million Population
fig1 = go.Figure(go.Choroplethmapbox(geojson=countries, locations=df1.country, z=df1.total_cases_per_1m_population,
                                    colorscale="Viridis", zmin=0, zmax=180000,
                                    marker_opacity=0.5, marker_line_width=0))
fig1.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=1, mapbox_center={"lat": 38.9637, "lon": 35.2433})
fig1.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})


# display
app.layout = html.Div([
    # chart 1
    html.H1("Covid-19 Cases Per Million Population",
            style={'text-align': 'center'}),

    dcc.Graph(
        id='case-per-million',
        figure=fig1
    ),
    html.Br(),


    # Chart 2: Daily New Case by Continent
    html.H1("Daily New Case by Continent",
            style={'text-align': 'center'}),

    dcc.Checklist(
        id="checklist",
        options=[{"label": x, "value": x}
                 for x in all_continents],
        value=all_continents,
        labelStyle={'display': 'inline-block'}
    ),
  
    dcc.Graph(id="line-chart"),
    
    
    # Chart 3: Cumulative Cases and Deaths
    html.H1("Cumulative Cases and Deaths",
            style={'text-align': 'center'}),

    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'January 2020', 'value': 'January 2020'},
            {'label': 'Feburary 2020', 'value': 'Feburary 2020'},
            {'label': 'March 2020', 'value': 'March 2020'},
            {'label': 'April 2020', 'value': 'April 2020'},
            {'label': 'May 2020', 'value': 'May 2020'},
            {'label': 'June 2020', 'value': 'June 2020'},
            {'label': 'July 2020', 'value': 'July 2020'},
            {'label': 'August 2020', 'value': 'August 2020'},
            {'label': 'September 2020', 'value': 'September 2020'},
            {'label': 'October 2020', 'value': 'October 2020'},
            {'label': 'November 2020', 'value': 'November 2020'},
            {'label': 'December 2020', 'value': 'December 2020'},
            {'label': 'January 2021', 'value': 'January 2021'},
            {'label': 'Feburary 2021', 'value': 'Feburary 2021'},
            {'label': 'March 2021', 'value': 'March 2021'},
            {'label': 'April 2021', 'value': 'April 2021'},
            {'label': 'May 2021', 'value': 'May 2021'},
            {'label': 'June 2021', 'value': 'June 2021'},
            {'label': 'July 2021', 'value': 'July 2021'},
        ],
        value='July 2021'
    ),

    dcc.Graph(id="scatter-plot"),

])

# callback function for Chart 2
@app.callback(
    Output("line-chart", "figure"),
    [Input("checklist", "value")])
def update_line_chart(continents):
    mask = df2.continent.isin(continents)
    fig = px.line(df2[mask], x="date",
                  y="daily_new_cases", color='country')

    return fig

# callback function for Chart 3
@app.callback(
    Output("scatter-plot", "figure"),
    [Input("dropdown", "value")])
def update_scatter_plot(val):
    mask = (df3.date == val)

    fig = px.scatter(
        df3[mask], x='cumulative_total_cases', y='cumulative_total_deaths',
        color='country',
        log_x=True)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)


