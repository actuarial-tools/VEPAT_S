import dash
import dash_html_components as html
import dash_core_components as dcc

volcanoSelect = html.Label(
                [
                    "Select Volcano",
                    dcc.Dropdown(
                        id='Volcano-dropdown',
                        options=[
                            {'label': 'Ruapehu', 'value': 'Ruapehu'},
                            {'label': 'Whakaari', 'value': 'Whakaari'},
                            {'label': 'Tongariro', 'value': 'Tongariro'}
                        ],
                        value='Whakaari'
                    ),
                ]
            )

questionSelect = html.Label(
                [
                    "Select Question",
                    dcc.Dropdown(
                        id='question-dropdown',
                        options=[
                            {'label': 'Ruapehu', 'value': 'Ruapehu'},
                            {'label': 'Whakaari', 'value': 'Whakaari'},
                            {'label': 'Tongariro', 'value': 'Tongariro'}
                        ],
                        value='Whakaari'
                    ),
                ])