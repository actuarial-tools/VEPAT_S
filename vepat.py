import dash
import dash_bootstrap_components as dbc
from dashBoardElements import dbElements

class mainApplication( object ):
    def run_server( self ):

        self.app.run_server(debug=True)

    def __init__( self ):
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

        # this class will become obsolete ? when we start using dash_bootstrap_components ?
        self.dbe = dbElements()

        # FOR GRIPD LAYOUTS TRY THIS: https://dash-bootstrap-components.opensource.faculty.ai/
        # bhttps: // dash - bootstrap - components.opensource.faculty.ai / l / components / layout
        self.app.layout = self.dbe.mainLayout()

        self.dbe.setQuestionForVolcano(self.app)

        self.run_server()

if __name__ == '__main__':
    ma = mainApplication()
