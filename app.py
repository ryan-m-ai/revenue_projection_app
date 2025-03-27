import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Set page config
st.set_page_config(
	page_title='Revenue Projection App',
	page_icon='💰',
	layout='wide'
)

# Sidebar inputs
with st.sidebar:
	st.header('Input Parameters')
	starting_revenue = st.number_input(
		'Starting Revenue ($)',
		min_value=0.0,
		value=100000.0,
		step=10000.0
	)
	growth_rate = st.number_input(
		'Annual Growth Rate (%)',
		min_value=-100.0,
		max_value=1000.0,
		value=10.0,
		step=1.0
	)
	years = st.number_input(
		'Projection Period (Years)',
		min_value=1,
		max_value=50,
		value=5,
		step=1
	)

# Main content
st.title('Revenue Projection Calculator')
st.markdown('''
	This app helps you project future revenue based on your assumptions.
	Adjust the parameters in the sidebar to see different projections.
''')

# Calculate projections
try:
	# Convert growth rate to decimal
	growth_rate_decimal = growth_rate / 100
	
	# Create year array
	year_array = np.arange(0, years + 1)
	
	# Calculate projected revenue using compound growth formula
	projected_revenue = starting_revenue * (1 + growth_rate_decimal) ** year_array
	
	# Create DataFrame for plotting
	df = pd.DataFrame({
		'Year': year_array,
		'Revenue': projected_revenue
	})
	
	# Create line chart
	fig = px.line(
		df,
		x='Year',
		y='Revenue',
		title='Revenue Projection Over Time',
		labels={'Revenue': 'Revenue ($)', 'Year': 'Years from Start'}
	)
	
	# Update layout for better readability
	fig.update_layout(
		plot_bgcolor='white',
		paper_bgcolor='white',
		showlegend=False
	)
	
	# Display the chart
	st.plotly_chart(fig, use_container_width=True)
	
	# Display summary statistics
	st.header('Summary Statistics')
	col1, col2, col3 = st.columns(3)
	
	with col1:
		st.metric(
			'Starting Revenue',
			f'${starting_revenue:,.2f}'
		)
	
	with col2:
		final_revenue = projected_revenue[-1]
		st.metric(
			'Final Projected Revenue',
			f'${final_revenue:,.2f}'
		)
	
	with col3:
		total_growth = ((final_revenue - starting_revenue) / starting_revenue) * 100
		st.metric(
			'Total Growth',
			f'{total_growth:.1f}%'
		)

except Exception as e:
	st.error(f'An error occurred: {str(e)}')
	st.info('Please check your input values and try again.') 