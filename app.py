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
server = app.server

USER_UID = ""

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
    ], id = "login-content", className = "login-page") #Container
])

# Login: Successful
#
@callback(
    Output('page-content', 'children'),
    Output('login-content', 'children'),
    Output('login-response', 'children'),
    Input('login-email', 'value'),
    Input('login-password', 'value'),
    Input('login-button', 'n_clicks')
)
def login_user(email, password, n_clicks) :
    print('Login function start')
    if n_clicks :
        print('login func: Registered click')
        try : 
            user = auth.sign_in_with_email_and_password(email, password)
            print('email + pass correct')
            global USER_UID
            USER_UID = user['localId']
            print(f"User's UID is: {USER_UID}")
            print(f"User's email is: {dataConfig[USER_UID]['user']}")
            print("Login successful. Returning dashboard.")
            return dashboard.layout, " ", " " # Return dashboard and hide login content
        except :
            print("Login failed")
            return " ", app.layout, "Your email or password is incorrect. Please try again :)"

# Run Server
#
if __name__ == '__main__':
    app.run_server(
        debug = True,
        dev_tools_hot_reload = False
    )
