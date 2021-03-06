from dash import Dash, dcc, html, callback
from dash import Input, Output
from authentication import auth
from data import get_data, create_areas_df
import plotly.graph_objs as go
import dash_bootstrap_components as boot
import plotly.express as px
import pandas as pd

pd.set_option("display.max_columns", None)

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
    html.Section([
        html.Header(
            boot.Container([
                boot.Row([
                    boot.Col([
                        boot.Row([
                            html.Img(src="assets/logo.svg")
                        ], className = 'header-logo', align='center')
                    ], width = 3),
                    boot.Col([
                        boot.Row([
                            html.Ul(
                                html.Li('Fake Name', id="nav-username")
                            )
                        ], className = 'header-nav', align='center')
                    ], width = 3)
                ], justify="between")
            ])
        ),
        boot.Container ([
            boot.Row([
                boot.Col([
                    html.Div([
                        html.H3('Login'),
                        html.Div([
                            boot.Label("Email", html_for="login-email"),
                            boot.Input(id = "login-email", type = "email", placeholder = "", autoFocus = "autofocus")
                        ], className = "mb-3"),

                        html.Div([
                            boot.Label("Password", html_for="login-password"),
                            boot.Input(id = "login-password", type = "password", placeholder = "")
                        ], className = "mb-4"),

                        boot.Button('Login', id = "login-button", color = "primary", className = "btn-full-width"),
                        boot.FormText(id = "login-response"),

                    ], className='card')
                ], width = 3)
            ], justify="center", align='center', className='login-page')
        ])
    ], id="login-content", className="login-page") # Section
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
            df_areas = create_areas_df(df)
            print(f"data returned from the user: {df}")
            print(f"areas dataframe is: {df_areas}")
            print("Login successful. Returning dashboard.")
            return dashboard, " ", " " # Return dashboard and hide login content
        except :
            print("Login failed")
            return " ", app.layout, "Your email or password is incorrect. Please try again :)"



dashboard = html.Div ([

    # HEADER
    # ...

    # CONTENT
    boot.Container([
        html.Div([

            # HEADING
            boot.Row(
                boot.Col(
                    html.H1('Life Areas')
                )
            ),

            # AREAS DROPDOWN
            boot.Row([
                boot.Col([
                    html.H6('Areas'),
                    dcc.Dropdown(
                        id = 'areas-dropdown',
                        options=[
                            {'label': 'Physical Health', 'value': 'area_score_physical_health'},
                            {'label': 'Mental Health', 'value': 'area_score_mental_health'},
                            {'label': 'Career', 'value': 'area_score_career'},
                            {'label': 'Finance', 'value': 'area_score_finance'},
                            {'label': 'Self Expression', 'value': 'area_score_self_expression'},
                            {'label': 'Relationship', 'value': 'area_score_relationship'},
                            {'label': 'Social', 'value': 'area_score_social'},
                            {'label': 'Family', 'value': 'area_score_family'},
                            {'label': 'Overall Life', 'value': 'area_score_overall_life'}
                        ],
                        multi = True,
                        value = ['area_score_physical_health', 'area_score_mental_health', 'area_score_career', 'area_score_finance', 'area_score_self_expression', 'area_score_relationship', 'area_score_social', 'area_score_family', 'area_score_overall_life'],

                    ),
                ]),
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
        ], className='card') # div
    ])
])


#------------
#------------ Update Graph 
#------------

@callback(
    Output('areas-graph','figure'),
    Input('areas-dropdown','value'),
    Input('average-slider','value'),
)
def update_areas_graph(selected_area, average_slider_value) :

    print(f"selected area is: {selected_area}")

    df_selection = df[selected_area] # Create new dataframe using dropdown selection
    df_selection = pd.DataFrame(df_selection)
    df_selection = pd.concat([df_selection, df['creation_date']], axis=1) # Append Date Column
    df_selection.set_index('creation_date', inplace = True) # Set Date as Index

    color_discrete_map = {
        'area_score_physical_health' : 'rgb(83,179,139)',
        'area_score_mental_health' : 'rgb(183,65,202)',
        'area_score_career' : 'rgb(123,97,255)',
        'area_score_finance' : 'rgb(42,90,215)',
        'area_score_self_expression' : 'rgb(99,208,239)',
        'area_score_relationship' : 'rgb(255,151,179)',
        'area_score_social' : 'rgb(236,97,97)',
        'area_score_family' : 'rgb(242,165,103)',
        'area_score_overall_life' : 'rgb(255,249,109)'
    }

    fig = px.scatter(
        df_selection,
        trendline = 'rolling',
        trendline_options = dict(window = average_slider_value),
        title = '{} point moving average'.format(average_slider_value),
        template = 'plotly_dark',
        height = 700,
        color_discrete_map = color_discrete_map,
    )

    fig.data = [t for t in fig.data if t.mode == "lines"]
    fig.update_traces(
        showlegend = True,
        line = dict(width = 1)
    )

    # Set legend names 
    newnames = {
        'area_score_physical_health' : 'Physical Health',
        'area_score_mental_health' : 'Mental Health',
        'area_score_career' : 'Career',
        'area_score_finance' : 'Finance',
        'area_score_self_expression' : 'Self Expression',
        'area_score_relationship' : 'Relationship',
        'area_score_social' : 'Social',
        'area_score_family' : 'Family',
        'area_score_overall_life' : 'Overall Life'
    }
    fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                        legendgroup = newnames[t.name],
                        hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
                        )
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
        debug = False,
        dev_tools_hot_reload = True
    ) 
