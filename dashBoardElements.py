import dash_core_components as dcc
from dash.dependencies import Input, Output

from myGuiElements import myDropDown, myContainer


class dbElements( object ):

	def __init__( self ):

		self.volcanoSelect = myDropDown( options=[ { 'label': 'Ruapehu', 'value': 'Ruapehu' },
												   { 'label': 'Whakaari', 'value': 'Whakaari' },
												   { 'label': 'Tongariro', 'value': 'Tongariro' } ],
										 id='Volcano-dropdown',
										 defaultValue='Whakaari' )

		self.questionSelect = myContainer( 'questions' )

		self.ruapehuQuestionSelect = myDropDown( id='ruapehuQuestionsDropDown',
												 options=[
													 { 'label': 'rq1', 'value': 'Ruapehu question 1 ?' },
													 { 'label': 'rq2', 'value': 'Ruapehu question 2 ?' },
													 { 'label': 'rq2', 'value': 'Ruapehu question 3 ?' }
												 ])

		self.whakaariQuestionSelect = myDropDown( id='whakaariQuestionsDropDown',
												  options=[
													  { 'label': 'wq1', 'value': 'Whakaari question 1 ?' },
													  { 'label': 'wq2', 'value': 'Whakaari question 2 ?' },
													  { 'label': 'wq2', 'value': 'Whakaari question 3 ?' }
												  ] )

		self.tongariroQuestionSelect = myDropDown( id='tongariroQuestionsDropDown',
												   options=[
													   { 'label': 'tq1', 'value': 'Tongariro question 1 ?' },
													   { 'label': 'tq2', 'value': 'Tongariro question 2 ?' },
													   { 'label': 'tq2', 'value': 'Tongariro question 3 ?' }
												   ])

		self.adminTab = dcc.Tab( label='Admin', children=[
			self.volcanoSelect.element,
			self.questionSelect.element
		] )

		self.reportTab = dcc.Tab( label='Report', children=[ ] )

		self.elicitationTab = dcc.Tab( label='Provide Elicitation', children=[ ] )

	def setQuestionForVolcano( self, app ):
		@app.callback( Output( self.questionSelect.id, 'children' ),
					   [ Input( self.volcanoSelect.id, 'value' ) ]
					   )
		def provideWhatever( input_value ):
			if input_value == 'Ruapehu':
				return self.ruapehuQuestionSelect.element
			if input_value == 'Whakaari':
				return self.whakaariQuestionSelect.element
			if input_value == 'Tongariro':
				return self.tongariroQuestionSelect.element
