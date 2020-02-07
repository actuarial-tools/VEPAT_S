import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output

from myGuiElements import myDropDown, myContainer


class dbElements(object):

    def mainLayout(self):
        return html.Div(children=[
            self.navbar(),
            dcc.Tabs([
                self.adminTab(),
                self.elicitationTab(),
                self.reportTab(),
            ])
        ])

    def adminTab(self):
        return dcc.Tab(label='Admin',
                       children=[
                           self.adminTabBody()
                       ])

    def elicitationTab(self):
        return dcc.Tab(label='Provide Elicitation',
                       children=[])

    def reportTab(self):
        return dcc.Tab(label='Report',
                       children=[])

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

    def navbar(self):
        return dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Link", href="#")),
                dbc.DropdownMenu(
                    nav=True,
                    in_navbar=True,
                    label="Menu",
                    children=[
                        dbc.DropdownMenuItem("Entry 1"),
                        dbc.DropdownMenuItem("Entry 2"),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem("Entry 3"),
                    ],
                ),
            ],
            brand="Demo",
            brand_href="#",
            sticky="top",
        )

    def adminTabBody(self):
        return dbc.Container(
            [
                dbc.Row(
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
                )
            ],
            className="mt-4",
        )

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
