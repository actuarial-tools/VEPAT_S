from tab1 import makeTab1
from tab2 import tab2
from vepatLib import addTabs

import dash
import dash_html_components as html
import dash_core_components as dcc
from datetime import datetime as dt

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

confirm = dcc.ConfirmDialogProvider(
    children=html.Button('Submit', id='button'),
    id='danger-danger',
    message='Danger danger! Are you sure you want to continue?'
)


input = [dcc.Input(id='input-box', type='text'),
              dcc.Input(id='input-box2', type='text'),
              dcc.DatePickerSingle(
                 id='date-picker-single',
                 date=dt(2000, 5, 10)
             )]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.Div(
        addTabs(name = 'tabs-example',
            tabIds=('tab-1-example', 'tab-2-example'),
            tabLabels=('Tab One', 'Tab Two')),
    ),
    html.Div(id='output-container-button',
             children='Enter a value and press submit'),

    html.Div(confirm)
])


@app.callback(
        dash.dependencies.Output('output-container-button', 'children'),
        [dash.dependencies.Input('button', 'n_clicks')],
        [dash.dependencies.State('input-box', 'value')])
def update_output(n_clicks, value):
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks
    )

@app.callback(dash.dependencies.Output('tabs-content-example', 'children'),
              [dash.dependencies.Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return makeTab1(app)
    elif tab == 'tab-2-example':
        return tab2

return tab1

if __name__ == '__main__':
    app.run_server(debug=True)