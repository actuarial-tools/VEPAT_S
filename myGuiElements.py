import dash_html_components as html
import dash_core_components as dcc


class myDropDown(object):

    def __init__(self, options, id, defaultValue = None):
        self.id = id
        self.element = html.Label(
            [
                "Select Volcano",
                dcc.Dropdown(
                    id=id,
                    options=options,
                    value=defaultValue
                ),
            ]
        )

class myContainer(object):
    def __init__(self, id):
        self.id = id
        self.element = html.Div(id=id)