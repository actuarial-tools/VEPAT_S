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


ruapehuQuestionSelect = html.Label(
                [
                    "Select Question",
                    dcc.Dropdown(
                        id='ruapehuQuestsionsDropDown',
                        options=[
                            {'label': 'rq1', 'value': 'Ruapehu question 1 ?'},
                            {'label': 'rq2', 'value': 'Ruapehu question 2 ?'},
                            {'label': 'rq2', 'value': 'Ruapehu question 3 ?'}
                        ]
                    ),
                ])

whakaariQuestionSelect= html.Label(
                [
                    "please select Question for Whakaari elicitation",
                    dcc.Dropdown(
                        id='whakaariQuestsionsDropDown',
                        options=[
                            {'label': 'wq1', 'value': 'Whakaari question 1 ?'},
                            {'label': 'wq2', 'value': 'Whakaari question 2 ?'},
                            {'label': 'wq2', 'value': 'Whakaari question 3 ?'}
                        ]
                    ),
                ])

tongariroQuestionSelect= html.Label(
                [
                    "please select Question for Tongariro elicitation",
                    dcc.Dropdown(
                        id='tongariroQuestsionsDropDown',
                        options=[
                            {'label': 'tq1', 'value': 'Tongariro question 1 ?'},
                            {'label': 'tq2', 'value': 'Tongariro question 2 ?'},
                            {'label': 'tq2', 'value': 'Tongariro question 3 ?'}
                        ]
                    ),
                ])
