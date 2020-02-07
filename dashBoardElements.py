from multiprocessing import active_children

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from adminTab import adminTab
from elicitationTab import elicitationTab
from reportTab import reportTab


class dbElements(object):

    def __init__(self):
        self.adminTab = adminTab(id = 'Admin')
        self.elicitationTab = elicitationTab(id = 'elictation')
        self.reportTab = reportTab( id = 'report')

    def mainLayout(self):
        return html.Div(children=[
            self.navbar(),
            dcc.Tabs([
                self.adminTab.element,
                self.elicitationTab.element,
                self.reportTab.element,
            ])
        ])

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
