import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output


class dbElements(object):

    def getWilma( self, keyVals ):
        options = []
        for key, val in keyVals.items():
            options.append( {'label':key,'value':val})

        return html.Label(
                [
                    "Select Volcano",
                    dcc.Dropdown(
                            id='Volcano-dropdown',
                            options=options,
                            value='Whakaari'
                    ),
                ]
        )

    def __init__(self):

        self.fred = 'questionsContainer'


        self.reportTab = dcc.Tab(label='Report', children=[])


        self.elicitationTab = dcc.Tab(label='Provide Elicitation', children=[])

        self.volcanoSelect = self.getWilma({'Ruapehu':'Ruapehu',
                                            'Whakaari':'Whakaari',
                                            'Tongariro':'Tongariro'})
        # html.Label(
        #                 [
        #                     "Select Volcano",
        #                     dcc.Dropdown(
        #                         id='Volcano-dropdown',
        #                         options=[
        #                             {'label': 'Ruapehu', 'value': 'Ruapehu'},
        #                             {'label': 'Whakaari', 'value': 'Whakaari'},
        #                             {'label': 'Tongariro', 'value': 'Tongariro'}
        #                         ],
        #                         value='Whakaari'
        #                     ),
        #                 ]
        #             )

        self.ruapehuQuestionSelect = html.Label(
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

        self.whakaariQuestionSelect= html.Label(
                        [
                            "please select Question for Whakaari ### elicitation",
                            dcc.Dropdown(
                                id='whakaariQuestsionsDropDown',
                                options=[
                                    {'label': 'wq1', 'value': 'Whakaari question 1 ?'},
                                    {'label': 'wq2', 'value': 'Whakaari question 2 ?'},
                                    {'label': 'wq2', 'value': 'Whakaari question 3 ?'}
                                ]
                            ),
                        ])

        self.tongariroQuestionSelect= html.Label(
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

        self.adminTab = dcc.Tab(label='Admin', children=[
                self.volcanoSelect,
                html.Div(id=self.fred)
            ])

    def myClosure(self, app):
        @app.callback(Output(self.fred, 'children'),
                      [Input('Volcano-dropdown', 'value')]
                      )
        def provideWhatever(input_value):
            if input_value == 'Ruapehu':
                return self.ruapehuQuestionSelect
            if input_value == 'Whakaari':
                return self.whakaariQuestionSelect
            if input_value == 'Tongariro':
                return self.tongariroQuestionSelect

