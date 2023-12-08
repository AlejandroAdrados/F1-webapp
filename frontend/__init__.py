import dash
from dash import html
import os
from app import app as server

basedir = os.path.abspath(os.path.dirname(__file__))
rootdir = os.path.abspath(os.path.join(basedir, os.pardir))
assetsdir = os.path.join(rootdir, 'frontend', 'assets')

app_dash = dash.Dash(requests_pathname_prefix="/dash/")
app_dash.css.config.serve_locally = True
app_dash.scripts.config.serve_locally = True
app_dash.title = 'F1 Dashboard'

from frontend.layout import layout
app_dash.layout = layout