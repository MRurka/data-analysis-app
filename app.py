from dash import Dash, dcc, html, callback
from dash import Input, Output
import dash_bootstrap_components as boot
from authentication import auth
import dashboard

app = Dash(
    __name__, 
    suppress_callback_exceptions = True, 
    external_stylesheets = [boot.themes.BOOTSTRAP],
)

app.layout = html.Div([
    html.Div(id='page-content'),
    boot.Container ([
        boot.Row(
            boot.Col([
                dcc.Input(id = "login-email", type = "email", placeholder = "email"),
                dcc.Input(id = "login-password", type = "password", placeholder = "password",),
                html.Button('Login', id = 'login-button'),
            ]),
        ),
    ], id = "login-content")
])

# Login
#
@callback(
    Output('page-content', 'children'),
    Output('login-content', 'children'),
    Input('login-email', 'value'),
    Input('login-password', 'value'),
    Input('login-button', 'n_clicks')
)
def login_user(email, password, n_clicks) :
    if n_clicks :
        try : 
            auth.sign_in_with_email_and_password(email, password)
            print("Login successful")
            return dashboard.layout, " " # Return dashboard and hide login content
        except :
            print("Login failed")

# Run Server
#
if __name__ == '__main__':
    app.run_server(debug = False)
