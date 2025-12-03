

import pandas as pd
import numpy as np
import matplotlib.pyplot as mat
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

# Including Dataset from Drive
df = pd.read_csv('CO2_emission_by_countries_MODIFICADO.csv')
df

#Delete rows with missing data
df = df.dropna(subset=["CO2 emission (Tons)","Year"])
#Making sure the variable Year is whole number
df ["Year"] = df ["Year"].astype(int)
df ["CO2 emission (Tons)"] = df ["CO2 emission (Tons)"].astype(float)

Countries = df["Country"].unique()
Years = df["Year"].unique()
emision_min = df["CO2 emission (Tons)"].min()
emision_max = df["CO2 emission (Tons)"].max()



# Creating app Dash with topic QUARTZ
external_stylesheets = [dbc.themes.QUARTZ]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Global CO₂ Emissions"

#Define the application layout
app.layout = dbc.Container([
    #Create a more beautiful and organized structure
    dbc.Row([html.H1("Global CO₂ Emissions")]),
    #Create a row with the title Global CO2 Emissions
    dbc.Row([
        dbc.Col([
            html.Label("Select a Country:", style={'color': 'black'}),
            #Text, filter
            dcc.Dropdown(
                id ='selector_country',
                #interactive selector, to show a list the options
                options = [{'label': Country, 'value': Country} for Country in Countries],
                style={'color': 'black'},
                persistence_type='session',
                #Generate an options list for to menú with info about the names countries
                value = df['Country'].unique()[0]
                #Unify the name of each country
            ) # <-- Cierre limpio del dcc.Dropdown
        ], width = 2), 
                
    

        dbc.Col([ #Creating colmn
            html.Label("Select the year range", style={'color': 'black'}), #Text
            dcc.RangeSlider(
            #Select a range the number like a year
                id = 'selector_year',
                #Component identifier.
                min = 1990, #Minimum value, far left
                max = 2020, #Maximum value, far right
                value = [1990, 2020],
                #Select the range between 1990 and 2020
                marks = {a: str(a) for a in range (1990, 2021)},
                #Create the labels by year
                step = 5
                #Advance year by year
            )], width = 5),
        

        dbc.Col([ #Creating colmn
            html.Label("Select emissions range (CO2):", style={'color': 'black'}), #Descriptive text
            dcc.RangeSlider(
                #Create a double slider, that is, one with two buttons that
                #allow you to select a range of values.
                id = 'selector_emision',
                #Component identifier
                min = emision_min, #Minimum allowed value
                max = emision_max, #Maximum allowed value
                value = [emision_min, emision_max], #Selected range
                marks = {i: f'{i/1e9:.0f}B' for i in range (int(emision_min), int(emision_max) + 1, 50000000000)},
                step =  100000000, # Increase by one unit
            )], width = 5),

            
    ]),
])
        dbc.Col([
            dbc.Col ([
                dcc.Graph(id = 'Graph_Bars_Emision_CO2')
            ]),
            dbc.Col([
                dcc.Graph(id = 'Graph_Cake_emision_CO2')
            ]),
            dbc.Col([
                dcc.Graph(id = 'Graph_Line_emision_CO2')
            ])
        ])

])

#Defining the callbacks
@app.callback(
    [Output('Graph_Bars_Emision_CO2', 'figure'), #Graphics to use with update
     Output('Graph_Cake_emision_CO2', 'figure'),
     Output('Graph_Line_emision_CO2', 'figure')], # Added comma here
    [Input('selector_country', 'value'), #Values ​​that the user selects
     Input('selector_year', 'value'),
     Input('selector_emision', 'value'),]
    # Removed Input('selector_feedback', 'value') as it's not defined in the layout
)
def update_graph(values_country, range_year, range_emision):
  #Filter the dataframe by the selected country
  df_filtered = df[df["Country"] == values_country ] # Corrected to use values_country
  df_filtered = df_filtered[(df_filtered["Year"] >= range_year[0]) & (df_filtered["Year"] <= range_year[1])] # Corrected year range
  #Filter only columns are in min and max values for the Year (1990-2020)
  df_filtered = df_filtered[(df_filtered["CO2 emission (Tons)"] >= range_emision[0]) & (df_filtered["CO2 emission (Tons)"] <= range_emision[1])]
  #Filter only CO2 emissions between min and max values

  #Using Plotly code here
  # ---------------------- GRAPH 1: BARS GRAPH ----------------------
  bars_graph = px.bar(
      df_filtered,
      x = "Year",
      y = "CO2 emission (Tons)",
      title= f"CO2 Emissions in {values_country}"
  )

  # ---------------------- GRAPH 2: CAKE GRAPH ----------------------
  cake_graph = px.pie(
      df_filtered,
      names = "Year",
      values = "CO2 emission (Tons)",
      title= f"Percentage of CO2 Emissions per year in {values_country}"
  )

  # ---------------------- GRAPH 2: LINE GRAPH ----------------------
  line_graph = px.line(
      df_filtered,
      x = "Year",
      y = "CO2 emission (Tons)",
      title= f"Evolution of CO2 Emissions in {values_country}" 
  )
  line_graph.update_traces(
      line=dict( 
          color = 'black',
          width = 4
          )
  )
          
  for fig in [bars_graph, cake_graph, line_graph]:
      fig.update_layout(
          plot_bgcolor='rgba(0, 0, 0, 0)',
          paper_bgcolor='rgba(0, 0, 0, 0)'
      )
  return bars_graph, cake_graph, line_graph
