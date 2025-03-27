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
		'Starting Revenue ($M)',
		min_value=0.0,
		value=1.0,
		step=0.1,
		format='%.1f'
	) * 1_000_000  # Convert to actual dollars
	
	ebitda_margin = st.number_input(
		'Starting EBITDA Margin (%)',
		min_value=0.0,
		max_value=100.0,
		value=20.0,
		step=1.0,
		format='%.1f'
	) / 100  # Convert to decimal
	
	growth_rate = st.number_input(
		'Annual Growth Rate (%)',
		min_value=-100.0,
		max_value=1000.0,
		value=10.0,
		step=1.0,
		format='%.1f'
	) / 100  # Convert to decimal
	
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
	This app helps you project future revenue and EBITDA based on your assumptions.
	Adjust the parameters in the sidebar to see different projections.
''')

# Calculate projections
try:
	# Create year array
	year_array = np.arange(0, years + 1)
	
	# Calculate projected revenue using compound growth formula
	projected_revenue = starting_revenue * (1 + growth_rate) ** year_array
	
	# Calculate projected EBITDA
	projected_ebitda = projected_revenue * ebitda_margin
	
	# Create DataFrame for plotting
	df = pd.DataFrame({
		'Year': year_array,
		'Revenue': projected_revenue,
		'EBITDA': projected_ebitda
	})
	
	# Create revenue chart
	fig_revenue = px.bar(
		df,
		x='Year',
		y='Revenue',
		title='Revenue Projection Over Time',
		labels={'Revenue': 'Revenue ($)', 'Year': 'Years from Start'}
	)
	
	# Update revenue chart layout
	fig_revenue.update_layout(
		plot_bgcolor='white',
		paper_bgcolor='white',
		showlegend=False
	)
	
	# Create EBITDA chart
	fig_ebitda = px.bar(
		df,
		x='Year',
		y='EBITDA',
		title='EBITDA Projection Over Time',
		labels={'EBITDA': 'EBITDA ($)', 'Year': 'Years from Start'}
	)
	
	# Update EBITDA chart layout
	fig_ebitda.update_layout(
		plot_bgcolor='white',
		paper_bgcolor='white',
		showlegend=False
	)
	
	# Display the charts side by side
	col1, col2 = st.columns(2)
	
	with col1:
		st.plotly_chart(fig_revenue, use_container_width=True)
	
	with col2:
		st.plotly_chart(fig_ebitda, use_container_width=True)
	
	# Display summary statistics
	st.header('Summary Statistics')
	col1, col2, col3, col4 = st.columns(4)
	
	with col1:
		st.metric(
			'Starting Revenue',
			f'${starting_revenue/1_000_000:.1f}M'
		)
	
	with col2:
		final_revenue = projected_revenue[-1]
		st.metric(
			'Final Projected Revenue',
			f'${final_revenue/1_000_000:.1f}M'
		)
	
	with col3:
		final_ebitda = projected_ebitda[-1]
		st.metric(
			'Final Projected EBITDA',
			f'${final_ebitda/1_000_000:.1f}M'
		)
	
	with col4:
		total_growth = ((final_revenue - starting_revenue) / starting_revenue) * 100
		st.metric(
			'Total Growth',
			f'{total_growth:.1f}%'
		)

except Exception as e:
	st.error(f'An error occurred: {str(e)}')
	st.info('Please check your input values and try again.') 