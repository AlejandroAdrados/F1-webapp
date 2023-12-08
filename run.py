# En el archivo run.py
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from app import app as app_flask
from frontend import app_dash

app_combined = DispatcherMiddleware(app_flask, {
    '/dash': app_dash.server
})

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 8050, app_combined)
