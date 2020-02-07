import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from myGuiElements import myDropDown, myContainer, myButton


class adminTab(object):
    def __init__(self, id):
        self.id = id
        self.element = dcc.Tab(label='Admin',
                               id=id,
                               children=[
                           self.adminTabBody()
                       ])

    def questionSelect(self):
        return myContainer(label='Please select a question for selected volcano ... ', id='questions')

    def tongariroQuestions(self):
        return myDropDown(id='tongariroQuestionsDropDown',
                          options=[
                              {'label': 'A question about Tongario 1', 'value': 'Tongariro question 1 ?'},
                              {'label': 'A question about Tongario 2', 'value': 'Tongariro question 2 ?'},
                              {'label': 'A question about Tongario 2', 'value': 'Tongariro question 3 ?'}
                          ])

    def whakaariQuestions(self):

        # return dbc.DropdownMenu(
        #     id='whakaariQuestionsDropDown',
        #     label="Menu",
        #     children=[
        #         dbc.DropdownMenuItem('A question about Whaakari  1', ),
        #         dbc.DropdownMenuItem('A question about Whaakari  2', ),
        #         dbc.DropdownMenuItem('A question about Whaakari  3', ),
        #         dbc.DropdownMenuItem('A question about Whaakari  4', ),
        #     ],
        # )

        return myDropDown(id='whakaariQuestionsDropDown',
                          options=[
                              {'label': 'A question about Whaakari  1', 'value': 'Whakaari question 1 ?'},
                              {'label': 'A question about Whaakari  2', 'value': 'Whakaari question 2 ?'},
                              {'label': 'A question about Whaakari  2', 'value': 'Whakaari question 3 ?'}
                          ])

    def ruapehuQuestions(self):
        return myDropDown(id='ruapehuQuestionsDropDown',
                          options=[
                              {'label': 'A question about Ruapehu 1', 'value': 'Ruapehu question 1 ?'},
                              {'label': 'A question about Ruapehu 2', 'value': 'Ruapehu question 2 ?'},
                              {'label': 'A question about Ruapehu 2', 'value': 'Ruapehu question 3 ?'}
                          ])

    def volcanoSelect(self):
        return myDropDown(label='Please select a volcano',
                          options=[{'label': 'Ruapehu', 'value': 'Ruapehu'},
                                   {'label': 'Whakaari', 'value': 'Whakaari'},
                                   {'label': 'Tongariro', 'value': 'Tongariro'}],
                          id='Volcano-dropdown',
                          defaultValue='Whakaari')

    def activeAdminBody(self):
        return [dbc.Row(
            [
                dbc.Col(
                    [
                        self.volcanoSelect().element,
                        self.questionSelect().element,
                        dbc.Button("View details", color="secondary"),
                    ],
                    md=4,
                ),
                dbc.Col(
                    [
                        html.H2("Graph"),
                        dcc.Graph(
                            figure={"data": [{"x": [1, 2, 3], "y": [1, 4, 9]}]}
                        ),
                    ]
                ),
            ]
        )]

    def adminTabBody(self):
        return self.deactiveatedAdminBody()

    def deactiveatedAdminBody(self):
        return myButton(id='activateButton', label='activate').element


    def activateAdminTab(self, app):
        @app.callback(Output("Admin", "children"),
                      [Input(self.deactiveatedAdminBody().id, "n_clicks")]
                      )
        def __activateAdminTab(n):
            if n is None:
                return self.deactiveatedAdminBody().element
            else:
                return self.activeAdminBody()

    def setQuestionForVolcano(self, app):
        @app.callback(Output(self.questionSelect().id, 'children'),
                      [Input(self.volcanoSelect().id, 'value')]
                      )
        def __setQuestionForVolcano(input_value):
            if input_value == 'Ruapehu':
                return self.ruapehuQuestions().element

            if input_value == 'Whakaari':
                return self.whakaariQuestions().element

            if input_value == 'Tongariro':
                return self.tongariroQuestions().element