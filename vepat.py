import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output


from dashBoardElements import volcanoSelect, ruapehuQuestionSelect, whakaariQuestionSelect, tongariroQuestionSelect

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Admin', children=[
            volcanoSelect,
            html.Div(id='questionsContainer')
        ]),
        dcc.Tab(label='Provide Elicitation', children=[
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [1, 4, 1],
                         'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [1, 2, 3],
                         'type': 'bar', 'name': u'Montréal'},
                    ]
                }
            )
        ]),
        dcc.Tab(label='Report', children=[
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [2, 4, 3],
                         'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [5, 4, 3],
                         'type': 'bar', 'name': u'Montréal'},
                    ]
                }
            )
        ]),
    ])
])

@app.callback(
    Output('questionsContainer', 'children'),
    [Input('Volcano-dropdown', 'value')])
def provideQuestionSetForVolcano(input_value):
    if input_value == 'Ruapehu':
        return ruapehuQuestionSelect
    if input_value == 'Whakaari':
        return whakaariQuestionSelect
    if input_value == 'Tongariro':
        return tongariroQuestionSelect


if __name__ == '__main__':
    app.run_server(debug=True)
