import dash_html_components as html
import dash_core_components as dcc

mapbox_access_token = 'need to get this form mapbox - I wonder if it is free ?'
# WORKING OF THIS EXAMPE https://medium.com/a-r-g-o/using-plotlys-dash-to-deliver-public-sector-decision-support-dashboards-ac863fa829fb

mapLayout = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
    title='Each dot is an NYC Middle School eligible for SONYC funding',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(
            lon=-73.91251,
            lat=40.7342
        ),
        zoom=10,
    )
)


# class myMap( object ):
# 	def __init__(self, options, id, defaultValue=None, label=None ):
#
#
# 		self.element = html.Div(
# 			[
# 				html.Div(
# 					[
# 						dcc.Graph(id='map-graph',
# 								  style={'margin-top': '20'})
# 					], className="six columns"
# 				),
# 				html.Div(
# 					[
# 						dt.DataTable(
# 							rows=map_data.to_dict('records'),
# 							columns=map_data.columns,
# 							row_selectable=True,
# 							filterable=True,
# 							sortable=True,
# 							selected_row_indices=[],
# 							id='datatable'),
# 					],
# 					style=layout_right,
# 					className="six columns"
# 				),
# 				html.Div(
# 					[
# 						dcc.Graph(id="histogram")
# 					], className="twelve columns")
# 			], className="row"
# 		)


class myDropDown(object):

    def __init__(self, options, id, defaultValue=None, label=None):
        self.id = id
        self.element = html.H4(
            [
                label,
                dcc.Dropdown(
                    id=id,
                    options=options,
                    value=defaultValue
                ),
            ]
        )


class myContainer(object):

    def __init__(self, id, label=None):
        self.id = id
        self.element = html.H4(
            [label,
             html.Div(id=id)
             ]
        )


class myGraph(object):

    def __init__(self, options, id, defaultValue=None, label=None):
        self.id = id
        self.element = html.Div(
            [
                label,
                dcc.Graph(
                    id=id,
                    options=options,
                    value=defaultValue,
                    className=None
                ),
            ]
        )
