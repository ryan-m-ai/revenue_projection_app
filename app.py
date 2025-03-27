import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# Set page config
st.set_page_config(
	page_title='Return Calculator',
	page_icon='💰',
	layout='wide',
	initial_sidebar_state='expanded'
)

# Custom CSS
st.markdown("""
	<style>
	.main {
		padding: 2rem;
	}
	.stMetric {
		background-color: #f0f2f6;
		padding: 1rem;
		border-radius: 0.5rem;
		margin-bottom: 1rem;
	}
	.stMetric:hover {
		background-color: #e6e9ef;
	}
	.stSubheader {
		font-size: 1.2rem;
		font-weight: 600;
		color: #1f1f1f;
		margin-bottom: 1rem;
		padding-bottom: 0.5rem;
		border-bottom: 2px solid #e6e9ef;
	}
	</style>
""", unsafe_allow_html=True)

# Sidebar inputs
with st.sidebar:
	st.header('Entry Assumptions')
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
	
	ev_ebitda_multiple = st.number_input(
		'Entry EV/EBITDA Multiple',
		min_value=0.0,
		max_value=100.0,
		value=10.0,
		step=1.0,
		format='%.1f'
	)
	
	st.markdown('---')
	st.header('Exit Assumptions')
	years = st.number_input(
		'Projection Period (Years)',
		min_value=1,
		max_value=50,
		value=5,
		step=1
	)
	
	growth_rate = st.number_input(
		'Annual Revenue Growth (%)',
		min_value=-100.0,
		max_value=1000.0,
		value=10.0,
		step=1.0,
		format='%.1f'
	) / 100  # Convert to decimal
	
	margin_improvement = st.number_input(
		'Annual EBITDA Margin Improvement (%)',
		min_value=-100.0,
		max_value=100.0,
		value=1.0,
		step=0.5,
		format='%.1f'
	) / 100  # Convert to decimal
	
	exit_multiple = st.number_input(
		'Exit EV/EBITDA Multiple',
		min_value=0.0,
		max_value=100.0,
		value=12.0,
		step=1.0,
		format='%.1f'
	)

# Main content
st.title('Return Calculator')
st.markdown('---')

# Calculate projections
try:
	# Create year array
	year_array = np.arange(0, years + 1)
	
	# Calculate projected revenue using compound growth formula
	projected_revenue = starting_revenue * (1 + growth_rate) ** year_array
	
	# Calculate projected EBITDA with margin improvement
	ebitda_margins = ebitda_margin * (1 + margin_improvement) ** year_array
	projected_ebitda = projected_revenue * ebitda_margins
	
	# Calculate entry and exit EV
	entry_ev = projected_ebitda[0] * ev_ebitda_multiple
	exit_ev = projected_ebitda[-1] * exit_multiple
	
	# Calculate return metrics
	return_multiple = exit_ev / entry_ev
	irr = (return_multiple ** (1/years) - 1) * 100
	
	# Create DataFrame for plotting
	df = pd.DataFrame({
		'Year': year_array,
		'Revenue': projected_revenue,
		'EBITDA': projected_ebitda,
		'EBITDA Margin': ebitda_margins * 100  # Convert to percentage for display
	})
	
	# Display metrics in three boxes
	col1, col2, col3 = st.columns(3)
	
	with col1:
		st.markdown('### Entry')
		st.metric(
			'Revenue',
			f'${starting_revenue/1_000_000:.1f}M'
		)
		st.metric(
			'EBITDA',
			f'${projected_ebitda[0]/1_000_000:.1f}M'
		)
		st.metric(
			'EBITDA Margin',
			f'{ebitda_margins[0]*100:.1f}%'
		)
	
	with col2:
		st.markdown('### Exit')
		st.metric(
			'Revenue',
			f'${projected_revenue[-1]/1_000_000:.1f}M'
		)
		st.metric(
			'EBITDA',
			f'${projected_ebitda[-1]/1_000_000:.1f}M'
		)
		st.metric(
			'EBITDA Margin',
			f'{ebitda_margins[-1]*100:.1f}%'
		)
	
	with col3:
		st.markdown('### Return')
		st.metric(
			'Return Multiple',
			f'{return_multiple:.1f}x'
		)
		st.metric(
			'IRR',
			f'{irr:.1f}%'
		)
	
	st.markdown('---')
	
	# Create revenue chart
	fig_revenue = px.bar(
		df,
		x='Year',
		y='Revenue',
		title='Revenue Projection Over Time',
		labels={'Revenue': 'Revenue ($)', 'Year': 'Years from Start'},
		text=df['Revenue'].apply(lambda x: f'${x/1_000_000:.1f}M')
	)
	
	# Update revenue chart layout
	fig_revenue.update_layout(
		plot_bgcolor='white',
		paper_bgcolor='white',
		showlegend=False,
		uniformtext_minsize=8,
		uniformtext_mode='hide',
		xaxis=dict(tickmode='linear', tick0=0, dtick=1),
		height=400,
		margin=dict(t=30, b=30, l=30, r=30)
	)
	
	# Create EBITDA chart
	fig_ebitda = px.bar(
		df,
		x='Year',
		y='EBITDA',
		title='EBITDA Projection Over Time',
		labels={'EBITDA': 'EBITDA ($)', 'Year': 'Years from Start'},
		text=df['EBITDA'].apply(lambda x: f'${x/1_000_000:.1f}M')
	)
	
	# Update EBITDA chart layout
	fig_ebitda.update_layout(
		plot_bgcolor='white',
		paper_bgcolor='white',
		showlegend=False,
		uniformtext_minsize=8,
		uniformtext_mode='hide',
		xaxis=dict(tickmode='linear', tick0=0, dtick=1),
		height=400,
		margin=dict(t=30, b=30, l=30, r=30)
	)
	
	# Display the charts side by side
	col1, col2 = st.columns(2)
	
	with col1:
		st.plotly_chart(fig_revenue, use_container_width=True)
	
	with col2:
		st.plotly_chart(fig_ebitda, use_container_width=True)

except Exception as e:
	st.error(f'An error occurred: {str(e)}')
	st.info('Please check your input values and try again.') 