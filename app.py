import dash  # pip install dash==1.19.0 or higher
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import datetime
import app
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import date, datetime
import dash_daq as daq


# Iris bar figure
def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H1("Driver and Truck Performance Engine" ,style={'textAlign': 'center','color':'white'}),
                ]
            ),
        ],
    )

tabHead = dbc.Nav(
    [   dbc.NavLink("TRUCKS GEOLOCATION CHARTS", href="/", active="exact"),
        dbc.NavLink("INDIVIDUAL TRUCK CHARTS", href="/Individual_trucks_charts", active="exact", style={'color':'white'}),
        dbc.NavLink("DECISION ENGINE", href="/Management_decision_engine", active="exact"),
        # dbc.NavLink("PHcourt Branch Control Charts", href="/Portharcourt_Branch_Control_Charts", active="exact"),
        # dbc.NavLink("Management Decision Engine", href="/Management_Decision_Engine", active="exact"),  
    ],style={'width': '80%','margin-bottom':'-3px'},
)


df = pd.read_csv('Trucks_dataset.csv')
df[['latitude', 'longitude']] = df['Coordinates/Address'].str.split(',', expand=True)

df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
df = df.replace(np.nan, 0, regex=True)
df['Voltage/Battery (V/%)'] = df['Voltage/Battery (V/%)'].map(lambda x: x.lstrip('+-').rstrip('V')).astype(float)

df['Date and Time'] = pd.to_datetime(df['Date and Time'],  infer_datetime_format=True)
df['datetime'] = pd.to_datetime(df['Date and Time'], format='%Y-%m-%d %H:%M')
df["date"] = pd.to_datetime(df['Date and Time'], format='%Y-%m-%d').dt.date
df["date"] = pd.to_datetime(df['date'], format='%Y-%m-%d')

df =df[df['latitude']!= 0.0]
df['number'] = range(1, len(df)+1)
df_tail = df.groupby('Plate_number').tail(1)



####################################################################################################
# 000 - DROPDOWN FOR TRUCK SELECTION 
####################################################################################################
#########################################################
truck_options = df_tail['Plate_number'].unique()

# options=[{'label':x , 'value':x} for x in all]
# options.append({'label': 'Select All', 'value': "all"})
def dropdowtruck():
     return html.Div([
          dbc.Card(
          dbc.CardBody([
            dcc.Dropdown(
                id="Plate_number",
                options=[{
                    'label': i,
                    'value': i
                } for i in truck_options] + [{'label':'All Trucks' , 'value':'All Trucks'}],
                value='All Trucks'),

                    ])
                )
     ])  





layout1 = dbc.Container([
    dbc.Row([

        dbc.Col([
            html.H1("Vehicle Telementry Driving Analysis", style={'textAlign':'center'})
            ], width={'size': 10}),
        dbc.Col([
        html.Div([
            html.H6("Select Dates:"),
                dcc.DatePickerSingle(
                    id='my-date-picker-startdate',
                    min_date_allowed=date(2023, 7, 1),
                    max_date_allowed = date.today(),
                    # max_date_allowed=date(2018, 1, 24),
                    initial_visible_month=date(2023, 7, 2),
                    date=date(2023, 7, 2)
                ),
        ])
    ], xs = 12 , sm = 12 , md = 12 , lg = 2 , xl = 2),

           ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.Div(id='live-update-text'),
                                    # dcc.Interval(
                                    # id='interval-component',
                                    # interval=1*6000, # in milliseconds
                                    # n_intervals=0)
                                ])
                            ], style={'height':'270px'})
                        ], style={'box-shadow': '4px 4px 30px 0px #CCC5F7, 6px -4px 12px 0px #CCC5F7'})
                    ], width=6),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.Div(id='live-update-text1'),
                                    # dcc.Interval(
                                    # id='interval-component',
                                    # interval=1*6000, # in milliseconds
                                    # n_intervals=0)
                                ])
                            ], style={'height':'270px'})
                        ], style={'box-shadow': '4px 4px 30px 0px #CCC5F7, 6px -4px 12px 0px #CCC5F7'})
                    ], width=6)
                ], className="mb-3"),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.Div(id='live-update-text2'),
                                    # dcc.Interval(
                                    # id='interval-component',
                                    # interval=1*6000, # in milliseconds
                                    # n_intervals=0)
                                ])
                            ], style={'height':'270px'})
                        ], style={'box-shadow': '4px 4px 30px 0px #CCC5F7, 6px -4px 12px 0px #CCC5F7'})
                    ], width=6),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.Div(id='live-update-text3'),
                                    # dcc.Interval(
                                    # id='interval-component',
                                    # interval=1*6000, # in milliseconds
                                    # n_intervals=0)
                                ])
                            ], style={'height':'270px'})
                        ], style={'box-shadow': '4px 4px 30px 0px #CCC5F7, 6px -4px 12px 0px #CCC5F7'})
                    ], width=6)
                ], ),
            ]),

        ], xs = 12 , sm = 12 , md = 12 , lg = 6 , xl = 4),

        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.Div([
                                html.H6("Select Dates:"),
                                dcc.DatePickerSingle(
                                    id='my-date-picker-start',
                                    min_date_allowed=date(2023, 7, 1),
                                    max_date_allowed = date.today(),
                                    # max_date_allowed=date(2018, 1, 24),
                                    initial_visible_month=date(2023, 7, 2),
                                    date=date(2023, 7, 2)
                                ),
                                dcc.DatePickerSingle(
                                    id='my-date-picker-end',
                                    min_date_allowed=date(2023, 7, 1),
                                    max_date_allowed = date.today(),
                                    # max_date_allowed=date(2018, 1, 24),
                                    initial_visible_month=date(2023, 7, 8),
                                    date=date(2023, 7, 8),
                                ),
                            ])
                        ]),
                        dbc.CardBody([
                            html.P("Get Driving Insights $ Select by Date"),
                            dcc.Graph(id="map-chart", config={'displayModeBar': True},),
                            # dcc.Interval(
                            # id='interval-component',
                            # interval=1*6000, # in milliseconds
                            # n_intervals=0)
                        ])
                    ], style={'box-shadow': '4px 4px 30px 0px #CCC5F7, 6px -4px 12px 0px #CCC5F7'})
                ], width=12),
            ])
        ], xs = 12 , sm = 12 , md = 12 , lg = 7 , xl = 7)
    ],className="mt-3", justify='center'),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.Div([
                        html.H5("Select Date Range:"),
                        html.Div([
                            dcc.DatePickerSingle(
                                id='my-date-picker-startt',
                                min_date_allowed=date(2023, 7, 1),
                                max_date_allowed = date.today(),
                                # max_date_allowed=date(2018, 1, 24),
                                initial_visible_month=date(2023, 7, 2),
                                date=date(2023, 7, 2)
                            ),
                            dcc.DatePickerSingle(
                                id='my-date-picker-endd',
                                min_date_allowed=date(2023, 7, 1),
                                max_date_allowed = date.today(),
                                # max_date_allowed=date(2018, 1, 24),
                                initial_visible_month=date(2023, 7, 2),
                                date=date(2023, 7, 2),
                            ),
                        ]),
                    ]),
                ]),
                dbc.CardBody([
                    html.Div([
                        dcc.Graph(id="line1-chart", config={'displayModeBar': True},
                                #   figure=px.bar(df, x='date', y='bpi').
                                #   update_layout(margin=dict(l=20, r=20, t=30, b=20))
                                    ),
                        dcc.Graph(id="line2-chart", config={'displayModeBar': True},
                                #   figure=px.bar(df, x='date', y='bpi').
                                #   update_layout(margin=dict(l=20, r=20, t=30, b=20))
                                    ),
                        dcc.Graph(id="line4-chart", config={'displayModeBar': True},
                                #   figure=px.bar(df, x='date', y='bpi').
                                #   update_layout(margin=dict(l=20, r=20, t=30, b=20))
                                    ),
                        # dcc.Interval(
                        # id='interval-component',
                        # interval=1*6000, # in milliseconds
                        # n_intervals=0)             
                    ], style={'overflow':'scroll', 'maxHeight':'320px'}),
                ])
            ], style={'box-shadow': '4px 4px 30px 0px #CCC5F7, 6px -4px 12px 0px #CCC5F7'})
        ],  xs = 12 , sm = 12 , md = 12 , lg = 11 , xl = 11)
    ], className="mt-3", justify='center',),

    dbc.Row(
        dbc.Col(html.Hr(style={'border': "20px solid gray"}),width=12)),

], fluid=True, style={'backgroundColor':'lightgrey'})

layout2 =dbc.Container([])


layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Vehicle Telementry Driving Analysis", style={'textAlign':'center'})
            ], width={'size': 10})
           ]),    

    dbc.Row([
        dbc.Col([
        
            dbc.Card([
                dbc.CardBody([
                    html.P("Get Driving Insights $ Select by Date"),
                    dcc.Graph(id="mapall-chart", config={'displayModeBar': True},),
                    dcc.Interval(
                    id='interval-component',
                    interval=1*6000, # in milliseconds
                    n_intervals=0)
                ])
            ], style={'box-shadow': '4px 4px 30px 0px #CCC5F7, 6px -4px 12px 0px #CCC5F7'})
        ], width=12),
    ]),


    dbc.Row(
        dbc.Col(html.Hr(style={'border': "20px solid gray"}),width=12)),

], fluid=True, style={'backgroundColor':'lightgrey'})




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
                )

server = app.server

# app = Dash(external_stylesheets=[dbc.themes.SLATE])
app.layout = html.Div([

    dbc.Card(
        dbc.CardBody([
            build_banner(),

            dbc.Row([
                 dbc.Col([
                     dropdowtruck()
                 ], xs = 12 , sm = 12 , md = 12 , lg = 3 , xl = 3),
                 dbc.Col([
                     tabHead
        #             dbc.NavLink([
        #             dcc.Link(page['name']+"  |  ", href=page['path'])
        #             for page in dash.page_registry.values()
        # ],),
                 ], xs = 12 , sm = 12 , md = 12 , lg = 9 , xl = 9)

            ], align='center'), 


     
        ]), color = '#000000', style={'margin-bottom':'-15px'}
    ),
    html.Hr(),

    # content of each page
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    # dash.page_container
    
])

####################################################################################################
# 000 - TAB CALLBACK
####################################################################################################
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return layout
    elif pathname == "/Individual_trucks_charts":
        return layout1
    elif pathname == "/Management_decision_engine":
        return layout2
    # elif pathname == "/Portharcourt_Branch_Control_Charts":
    #     return layout3
    # elif pathname == "/Management_Decision_Engine":
    #     return Decision
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    ),



# Update Graph ***********************************************************
@app.callback(
    Output('map-chart','figure'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
    Input('Plate_number', 'value'),
    # Input('interval-component', 'n_intervals'),
)
def update_graph(start_date, end_date, Plate_number):
    dff1 = df[(df.date >= start_date) & (df.date <= end_date)]
    
    if Plate_number != "All Trucks":
            dff= df[df['Plate_number']==Plate_number]
            dff1 = dff[(dff.date >= start_date) & (dff.date <= end_date)]


    # if Plate_number == "All Trucks":
    #         dff1 = df.copy()
    # else:
    #     dff1 = df[df['Plate_number'] == Plate_number]
   
    fig = px.scatter_mapbox(dff1,
                        lon = dff1['longitude'],
                        lat = dff1['latitude'],
                        zoom = 11,
                        color = dff1['Speed (Km/h)'],
                            size = dff1['Mileage (Km)'],
                            # width = 900,
                            height = 400,
                            title = 'Route')

    fig.update_layout(mapbox_style = 'open-street-map')
    fig.update_layout(margin = {'r':0, 't':0, 'l':0, 'b':0})

    fig.add_traces(px.line_mapbox(dff1, lat=dff1['latitude'], lon=dff1['longitude'],).data)

    return fig

# Update GraphAll ***********************************************************
#    Input('my-date-picker-start','date'),

@app.callback(
    Output('mapall-chart','figure'),
    Input('Plate_number', 'value'),
    Input('interval-component', 'n_intervals'),
)

def update_graphAll(Plate_number, n):
    if Plate_number == "All Trucks":
        dff1 = df_tail.copy()
    else:
        dff1 = df_tail[df_tail['Plate_number'] == Plate_number]
    
    figall = px.scatter_mapbox(dff1,
                    lon = dff1['longitude'],
                    lat = dff1['latitude'],
                    zoom = 11,
                    color = dff1['Speed (Km/h)'],
                        size = dff1['Mileage (Km)'],
                        # width = 900,
                        height = 500,
                        title = 'Route')

    figall.update_layout(mapbox_style = 'open-street-map')
    figall.update_layout(margin = {'r':0, 't':0, 'l':0, 'b':0})

    return figall


@app.callback(
    Output('line1-chart','figure'),
    Output('line2-chart','figure'),
    Output('line4-chart','figure'),
    Input('my-date-picker-startt','date'),
    Input('my-date-picker-endd','date'),
    Input('Plate_number', 'value'),
    # Input('interval-component', 'n_intervals'),
)
def update_graph1(start_date, end_date, Plate_number):
    
    dff1 = df[(df.date >= start_date) & (df.date <= end_date)]
    
    if Plate_number != "All Trucks":
            dff= df[df['Plate_number']==Plate_number]
            dff1 = dff[(dff.date >= start_date) & (dff.date <= end_date)]
    # dff = df.copy()
    # dff2 = dff[(dff.date >= start_date1) & (dff.date <= end_date1)]
    # dff.loc[((dff.date>=start_date) & (dff.date<=end_date)), 'colors'] = 'black'

    fig1 = px.line(dff1, y='Speed (Km/h)', x='datetime', title ='SPEED WITH TIME')
    fig1.update_traces( line_color='#FF5E5E')
    fig1.update_layout(margin = {'r':0, 't':0, 'l':0, 'b':0}, height=300,width=3500,)


    fig2 = px.line(dff1, y='Fuel (A/D Value /L)', x='Mileage (Km)', title ='FUEL CONSUMPTION WITH DISTANCE')
    fig2.update_traces( line_color='#FF5E5E')
    fig2.update_layout(margin = {'r':0, 't':0, 'l':0, 'b':0}, height=300,width=3500,)

    fig4 = px.line(dff1, y='Fuel (A/D Value /L)', x='datetime', title ='FUEL CONSUMPTION TEMP WITH TIME')
    fig4.update_traces( line_color='#FF5E5E')
    fig4.update_layout(margin = {'r':0, 't':0, 'l':0, 'b':0}, height=300, width=3500,)

    return fig1, fig2, fig4

@app.callback(
    Output('live-update-text', 'children'),
    Input('my-date-picker-startdate','date'),
    Input('Plate_number', 'value'),
    # Input('interval-component', 'n_intervals')
)
def update_metrics(start_datee, Plate_number):
    dff1 = df[(df.date >= start_datee)]
    
    if Plate_number != "All Trucks":
        dff= df[df['Plate_number']==Plate_number]
        dff1 = dff[(df.date >= start_datee)]

    mileage = dff1["Mileage (Km)"].iloc[-1].round(),
    def engineTemp():
        temp_value = dff1["Temperature (?)"].iloc[-1]
        return temp_value

    
    return [
            html.P(str(datetime.now().strftime("%H:%M:%S"))),
            daq.LEDDisplay(
            label= "TRUCK MILEAGE",
            value= mileage,
            size=18,
            color="#FF5E5E",
            backgroundColor="#080134"
            ),
            html.Br(),
            daq.LEDDisplay(
            label= "ENGINE TEMP",
            value= engineTemp(),
            size=18,
            color="#FF5E5E",
            backgroundColor="#080134"
            ),
    ]


@app.callback(
        Output('live-update-text1', 'children'),
        Input('my-date-picker-startdate','date'),
        Input('Plate_number', 'value'),
        # Input('interval-component', 'n_intervals')
)
def update_metrics(start_datee, Plate_number):
    dff1 = df[(df.date >= start_datee)]
    
    if Plate_number != "All Trucks":
        dff= df[df['Plate_number']==Plate_number]
        dff1 = dff[(df.date >= start_datee)]

    def speedlValue():
        speed_value  = dff1["Fuel (A/D Value /L)"].iloc[-1]
        return speed_value
    
    return [
            html.P(str(datetime.now().strftime("%H:%M:%S"))),
            daq.Gauge(
            showCurrentValue=True,
            label='TRUCK SPEED',
            size=125,
            units="MPH",
            color="#FF5E5E",
            value= speedlValue(),
            max=220,
            min=0,)
]

@app.callback(
        Output('live-update-text2', 'children'),
        Input('my-date-picker-startdate','date'),
        Input('Plate_number', 'value'),
        # Input('interval-component', 'n_intervals')
)
def update_metrics(start_datee, Plate_number):
    dff1 = df[(df.date >= start_datee)]
    
    if Plate_number != "All Trucks":
        dff= df[df['Plate_number']==Plate_number]
        dff1 = dff[(df.date >= start_datee)]

    def fuelValue():
        fuel_value  = dff1["Fuel (A/D Value /L)"].iloc[-1]
        return fuel_value
    
    return [
            html.P(str(datetime.now().strftime("%H:%M:%S"))),
            daq.Tank(
            value= fuelValue(),
            showCurrentValue=True,
            label='FUEL LEVEL',
            units='Litres',
            height=125,
            width=90,
            max=50,
            min=0,
            color="#080134",
            style={'margin-left': '50px'})
    ]

@app.callback(
        Output('live-update-text3', 'children'),
        Input('my-date-picker-startdate','date'),
        Input('Plate_number', 'value'),
        # Input('interval-component', 'n_intervals')

)
def update_metrics(start_datee, Plate_number):
    dff1 = df[(df.date >= start_datee)]
    
    if Plate_number != "All Trucks":
        dff= df[df['Plate_number']==Plate_number]
        dff1 = dff[(df.date >= start_datee)]

    def engineTemp():
        temp_value = dff1["Temperature (?)"].iloc[-1]
        return temp_value
    def batteryValue():
        battery_value = dff1["Voltage/Battery (V/%)"].iloc[-1]
        return battery_value
    
    return [
            html.P(str(datetime.now().strftime("%H:%M:%S"))),
            daq.LEDDisplay(
            label= "BATTRY VOLTAGE",
            value= batteryValue(),
            size=18,
            color="#FF5E5E",
                backgroundColor="#080134"),
            html.Br(),
            daq.LEDDisplay(
            label= "ENGINE TEMP",
            value= engineTemp(),
            size=18,
            color="#FF5E5E",
            backgroundColor="#080134"),
]


if __name__ == "__main__":
    app.run_server(debug=False, port=8002)
