import dash_html_components as html
import dash_core_components as dcc


class myDropDown( object ):

	def __init__( self, options, id, defaultValue=None, label=None ):
		self.id = id
		self.element = html.Label(
			[
				label,
				dcc.Dropdown(
					id=id,
					options=options,
					value=defaultValue
				),
			]
		)


class myContainer( object ):

	def __init__( self, id, label=None ):
		self.id = id
		self.element = html.Label(
			[ label,
			  html.Div( id=id )
			  ]
		)


class myGraph( object ):

	def __init__( self, options, id, defaultValue=None, label=None ):
		self.id = id
		self.element = html.Div(
			[
				label,
				dcc.Graph(
					id=id,
					options=options,
					value=defaultValue
				),
			]
		)
