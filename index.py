import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from layouts import layout, layout_menu, layout2, layoutEconomy, layoutLE, layoutRevenueLE

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return layout_menu

    elif pathname == '/app1':
        return layout
    elif pathname == '/app2':
        return layout2
    elif pathname == '/economy':
        return layoutEconomy
    elif pathname == '/le':
        return layoutLE
    elif pathname == '/revLE':
        return layoutRevenueLE
    else:
        return '404'

if __name__ == '__main__':
    app.run_server()