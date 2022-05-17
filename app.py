from dash import Dash, dcc, html, callback
from dash import Input, Output
import dash_bootstrap_components as boot
from authentication import auth
from data import get_data
from datetime import date
import plotly.graph_objs as go
import dash_bootstrap_components as boot
import plotly.express as px
import pandas as pd

app = Dash(
    __name__, 
    suppress_callback_exceptions = True, 
    external_stylesheets = [boot.themes.BOOTSTRAP],
)
server = app.server

USER_UID = ""
df = []
df_areas = []

app.layout = html.Div([
    html.Div(id='page-content'),
    boot.Container ([
        boot.Row([
            boot.Col([
                html.Div([
                    html.Img(src="assets/logo.svg")
                ], className = "login-logo"),
       
                html.Div([
                    boot.Label("Email", html_for="login-email"),
                    boot.Input(id = "login-email", type = "email", placeholder = "", autoFocus = "autofocus")
                ], className = "mb-3"),

                html.Div([
                    boot.Label("Password", html_for="login-password"),
                    boot.Input(id = "login-password", type = "password", placeholder = "")
                ], className = "mb-3"),

                boot.Button('Login', id = "login-button", color = "primary", className = "btn-full-width"),
                boot.FormText(id = "login-response"),
            ], width = 3 ), # Col
            
        ], justify="center" ), # Row
    ], id = "login-content", className = "login-page")
])

dashboard = boot.Container ([
    
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
                options=[
                    {'label': 'area_score_physical', 'value': 'area_score_physical_health'},
                    {'label': 'Mental Health', 'value': 'area_score_mental_health'},
                    {'label': 'Career', 'value': 'area_score_career'},
                    {'label': 'Finance', 'value': 'area_score_finance'},
                    {'label': 'Self Expression', 'value': 'area_score_self_expression'},
                    {'label': 'Relationship', 'value': 'area_score_relationship'},
                    {'label': 'Social', 'value': 'area_score_social'},
                    {'label': 'Family', 'value': 'area_score_family'},
                    {'label': 'Overall Life', 'value': 'area_score_overall_life'}
                ],
                value = '',
                multi = True,
            ),
        ]),
        # boot.Col([
        #     html.H6('Date Range'),
        #     dcc.DatePickerRange(
        #         id = 'date-picker',
        #         display_format='MMM D, YYYY',
        #         max_date_allowed = date.today(),
        #         # end_date = date.today(),
        #         start_date_placeholder_text = 'Start date',
        #         end_date_placeholder_text = 'End date',
        #         first_day_of_week = 1, # Set calendar to Mon - Sun
        #         clearable = True, # Show 'X' in UI to clear
        #         day_size = 39, # Rendered calendar size
        #     ),
        # ]),
        boot.Col([
            html.H6('Moving Average Value'),
            dcc.Slider(
                id = 'average-slider',
                min = 1,
                max = 60,
                step = 1,
                value = 1,
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
                        xaxis = {'title' : 'creation_date'},
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
#------------ Login 
#------------

@callback(
    Output('page-content', 'children'),
    Output('login-content', 'children'),
    Output('login-response', 'children'),
    Input('login-email', 'value'),
    Input('login-password', 'value'),
    Input('login-button', 'n_clicks')
)
def login_user(email, password, n_clicks) :
    print('check_credentials function called')
    if n_clicks :
        print('Click registered')
        try : 
            user = auth.sign_in_with_email_and_password(email, password)
            print('email + pass correct')
            global USER_UID
            USER_UID = user['localId']
            print(f"User's UID is: {USER_UID}")
            global df
            df = get_data('life_areas', 'created_by', USER_UID)
            global df_areas
            df_areas = get_data('life_areas', 'created_by', USER_UID)
            print(f"data returned from the user: {df}")
            print("Login successful. Returning dashboard.")
            return dashboard, " ", " " # Return dashboard and hide login content
        except :
            print("Login failed")
            return " ", app.layout, "Your email or password is incorrect. Please try again :)"


#------------
#------------ Update Graph 
#------------

@callback(
    Output('areas-graph','figure'),
    Input('areas-dropdown','value'),
    Input('average-slider','value'),
    # Input('date-picker', 'start_date'),
    # Input('date-picker', 'end_date'),
)
def update_areas_graph(selected_area, average_slider_value) :

    print(f"selected area is: {selected_area}")

    df_selection = df[selected_area] # Create new dataframe using dropdown selection
    df_selection = pd.DataFrame(df_selection)

    print("—————————————— ONE ")
    print(df_selection)

    df_selection = pd.concat([df_selection, df['creation_date']], axis=1)

    print("—————————————— TWO ")
    print(df_selection)

    # Replace start & end dates with min/max when datepicker is empty
    # if start_date == None :
    #     start_date = df_selection['creation_date'].min()
    # if end_date == None :
    #     end_date = df_selection['creation_date'].max()

    print("—————————————— THREE ")
    print(df_selection)

    # Filter dataframe by date range
    # ——————————————————— Something here doesn't work. 
    # df_selection = df_selection[(df_selection['creation_date'] >= start_date) & (df_selection['creation_date'] <= end_date)]

    # print("—————————————— FOUR ")
    # print(df_selection)

    df_selection.set_index('creation_date', inplace = True) # Set Date as Index

    print("—————————————— FIVE ")
    print(df_selection)

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
    stats = """ {} """.format(df.iloc[v_index]['day_journal'])
    return stats


# Run Server
if __name__ == '__main__':
    app.run_server(
        debug = True,
        dev_tools_hot_reload = False
    )
