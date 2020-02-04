import dash
import dash_html_components as html
import dash_core_components as dcc

from dashBoardElements import dbElements

class mainApplication( object ):
    def run_server( self ):

        self.app.run_server(debug=True)

    def __init__( self ):
        self.external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

        self.app = dash.Dash(__name__, external_stylesheets=self.external_stylesheets)

        self.dbe = dbElements()

        self.app.layout = html.Div([
            dcc.Tabs([
                self.dbe.adminTab,
                self.dbe.elicitationTab,
                self.dbe.reportTab,
            ])
        ])

        self.dbe.myClosure(self.app)

        self.run_server()

# class OtherOne( object ):
#     def myClosure( self, app, dbe ):
#         @app.callback(Output( dbe.fred, 'children'),
#                            [Input('Volcano-dropdown', 'value')]
#                            )
#         def provideWhatever( input_value ):
#             if input_value == 'Ruapehu':
#                 return dbe.ruapehuQuestionSelect
#             if input_value == 'Whakaari':
#                 return dbe.whakaariQuestionSelect
#             if input_value == 'Tongariro':
#                 return dbe.tongariroQuestionSelect


if __name__ == '__main__':
    ma = mainApplication()
