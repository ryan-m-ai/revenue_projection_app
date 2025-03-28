import streamlit as st
from .ui import load_css, render_sidebar, render_metrics, render_charts, render_sensitivity
from .calculations import calculate_projections, calculate_sensitivity

def main():
	# Set page config
	st.set_page_config(
		page_title='Return Calculator',
		page_icon='💰',
		layout='wide',
		initial_sidebar_state='expanded'
	)

	# Load CSS
	load_css()

	# Main content
	st.title('Return Calculator')
	st.markdown('---')

	try:
		# Get inputs from sidebar
		inputs = render_sidebar()
		
		# Calculate projections
		results = calculate_projections(**inputs)
		
		# Render metrics
		render_metrics(
			results['entry_metrics'],
			results['exit_metrics'],
			results['return_metrics']
		)
		
		# Render charts
		render_charts(results['df'])
		
		# Calculate and render sensitivity analysis
		sensitivity_df = calculate_sensitivity(
			inputs['starting_revenue'],
			inputs['ebitda_margin'],
			inputs['ev_ebitda_multiple'],
			inputs['net_debt_entry'],
			inputs['net_debt_exit'],
			inputs['transaction_fees_exit'],
			results['entry_metrics']['equity'],
			inputs['years'],
			inputs['growth_rate'],
			inputs['exit_multiple']
		)
		render_sensitivity(sensitivity_df)

	except Exception as e:
		st.error(f'An error occurred: {str(e)}')
		st.info('Please check your input values and try again.')

if __name__ == '__main__':
	main() 