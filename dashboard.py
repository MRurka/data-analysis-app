from dash import dcc, html, callback
from dash import Input, Output
from datetime import date
from app import df, df_areas

import plotly.graph_objs as go
import dash_bootstrap_components as boot
import plotly.express as px


#------------
#------------ Layout
#------------

layout = boot.Container ([
    
    boot.Row(
        boot.Col(
            html.H1('Life Areas')
        )
    ),
    boot.Row([
        boot.Col([
            html.H6('Areas'),
            dcc.Dropdown(
                id = 'areas-dropdown',
                options = [{'label' : i, 'value' : i} for i in df_areas],
                value = df_areas,
                multi = True,
            ),
        ]),
        boot.Col([
            html.H6('Date Range'),
            dcc.DatePickerRange(
                id = 'date-picker',
                display_format='MMM D, YYYY',
                max_date_allowed = date.today(),
                # end_date = date.today(),
                start_date_placeholder_text = 'Start date',
                end_date_placeholder_text = 'End date',
                first_day_of_week = 1, # Set calendar to Mon - Sun
                clearable = True, # Show 'X' in UI to clear
                day_size = 39, # Rendered calendar size
            ),
        ]),
        boot.Col([
            html.H6('Moving Average Value'),
            dcc.Slider(
                id = 'average-slider',
                min = 1,
                max = 60,
                step = 1,
                value = 12,
                marks = None
            ),
        ])
    ]),
    boot.Row(
        boot.Col(
            dcc.Graph(
                id = 'areas-graph',
                figure = {
                    'layout' : go.Layout(
                        title = 'Life Areas',
                        xaxis = {'title' : 'Date'},
                        yaxis = {'title' : 'Score'},
                        paper_bgcolor = 'rgba(0,0,0,0)',
                        plot_bgcolor = 'rgba(0,0,0,0)'
                    )
                },
                config={
                    'displayModeBar': False
                }
            )
        )
    ),
    boot.Row(
        boot.Col(
            dcc.Markdown(id = 'daily-journal')
        )
    ),
    boot.Row(
        boot.Col([
            html.Button(id = 'db-test-button'),
            html.Div(id="db-test-response")
        ])
    ),
])

#------------
#------------ Test DB
#------------

@callback(
    Output('db-test-response','children'),
    Input('db-test-button','n_clicks')
)
def check_database():
    pass

#------------
#------------ Update Graph 
#------------

@callback(
    Output('areas-graph','figure'),
    Input('areas-dropdown','value'),
    Input('average-slider','value'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
)
def update_areas_graph(selected_area, average_slider_value, start_date, end_date) :

    df_selection = df[selected_area] # Create new dataframe using dropdown selection
    df_selection = df_selection.join(df['Date']) # Add Date to Selection dataframe

    # Replace start & end dates with min/max when datepicker is empty
    if start_date == None :
        start_date = df_selection['Date'].min()
    if end_date == None :
        end_date = df_selection['Date'].max()

    # Filter dataframe by date range
    df_selection = df_selection[(df_selection['Date'] > start_date) & (df_selection['Date'] < end_date)]
    df_selection.set_index('Date', inplace = True) # Set Date as Index

    print(df_selection.head)

    fig = px.scatter(
        df_selection,
        trendline = 'rolling',
        trendline_options = dict(window = average_slider_value),
        title = '{} point moving average'.format(average_slider_value),
        template = 'plotly_dark',
        height = 700
    )
    fig.data = [t for t in fig.data if t.mode == "lines"]
    fig.update_traces(
        showlegend = True,
        line = dict(width = 1)
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

#------------
#------------ Show Journal Entry on Hover
#------------

@callback(
    Output('daily-journal','children'),
    Input('areas-graph','hoverData')
)
def display_journal(hoverData) :
    v_index = hoverData['points'][0]['pointIndex']
    stats = """ {} """.format(df.iloc[v_index]['What happened?'])
    return stats

