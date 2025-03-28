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
		background-color: #f8f9fa;
		padding: 0.25rem;
		margin-bottom: 0.25rem;
		font-size: 0.875rem;
		height: 1.5rem;
		display: flex;
		align-items: center;
		border-radius: 0.25rem;
	}
	.stMetric:hover {
		background-color: #f0f2f6;
	}
	.stSubheader {
		font-size: 1rem;
		font-weight: 600;
		color: #1f1f1f;
		margin-bottom: 0.5rem;
		padding-bottom: 0.25rem;
		border-bottom: 1px solid #e6e9ef;
	}
	.stMarkdown {
		font-size: 0.875rem;
	}
	/* Style for metric values */
	.stMarkdown p {
		margin: 0;
		padding: 0.25rem;
		height: 1.5rem;
		display: flex;
		align-items: center;
		font-size: 0.875rem;
	}
	/* Style for metric headers */
	.stMarkdown h3 {
		font-size: 1rem;
		font-weight: 600;
		color: #1f1f1f;
		margin-bottom: 0.5rem;
		padding-bottom: 0.25rem;
		border-bottom: 1px solid #e6e9ef;
	}
	/* Style for dividers */
	hr {
		margin: 1rem 0;
		border: none;
		border-top: 1px solid #e6e9ef;
	}
	/* Style for charts */
	.js-plotly-plot {
		background-color: white !important;
	}
	/* Style for dataframe */
	.dataframe {
		background-color: white;
		border: 1px solid #e6e9ef;
		border-radius: 0.5rem;
		padding: 1rem;
		font-size: 0.875rem;
	}
	/* Style for sidebar */
	.css-1d391kg {
		background-color: #f8f9fa;
		padding: 1rem;
	}
	/* Style for number inputs */
	.stNumberInput input {
		background-color: white;
		border: 1px solid #e6e9ef;
		border-radius: 0.25rem;
		padding: 0.25rem;
		font-size: 0.875rem;
	}
	/* Style for headers */
	h1 {
		color: #1f1f1f;
		font-weight: 600;
		margin-bottom: 1rem;
		font-size: 1.5rem;
	}
	/* Style for error messages */
	.stAlert {
		background-color: #fff5f5;
		border: 1px solid #feb2b2;
		border-radius: 0.5rem;
		padding: 1rem;
		font-size: 0.875rem;
	}
	/* Style for info messages */
	.stInfo {
		background-color: #f0f9ff;
		border: 1px solid #bae6fd;
		border-radius: 0.5rem;
		padding: 1rem;
		font-size: 0.875rem;
	}
	/* Style for metric labels */
	.stMetric [data-testid="stMetricLabel"] {
		font-size: 0.875rem;
	}
	/* Style for metric values */
	.stMetric [data-testid="stMetricValue"] {
		font-size: 0.875rem;
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
	
	net_debt_entry = st.number_input(
		'Net Debt at Entry ($M)',
		min_value=0.0,
		value=0.0,
		step=0.1,
		format='%.1f'
	) * 1_000_000
	
	working_capital_entry = st.number_input(
		'Working Capital at Entry ($M)',
		min_value=0.0,
		value=0.0,
		step=0.1,
		format='%.1f'
	) * 1_000_000
	
	transaction_fees_entry = st.number_input(
		'Entry Transaction Fees (%)',
		min_value=0.0,
		max_value=10.0,
		value=1.0,
		step=0.1,
		format='%.1f'
	) / 100
	
	management_rollover = st.number_input(
		'Management Rollover (%)',
		min_value=0.0,
		max_value=100.0,
		value=0.0,
		step=1.0,
		format='%.1f'
	) / 100
	
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
	
	net_debt_exit = st.number_input(
		'Net Debt at Exit ($M)',
		min_value=0.0,
		value=0.0,
		step=0.1,
		format='%.1f'
	) * 1_000_000
	
	working_capital_exit = st.number_input(
		'Working Capital at Exit ($M)',
		min_value=0.0,
		value=0.0,
		step=0.1,
		format='%.1f'
	) * 1_000_000
	
	transaction_fees_exit = st.number_input(
		'Exit Transaction Fees (%)',
		min_value=0.0,
		max_value=10.0,
		value=1.0,
		step=0.1,
		format='%.1f'
	) / 100

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
	
	# Calculate entry and exit equity values
	entry_equity = entry_ev - net_debt_entry
	exit_equity = exit_ev - net_debt_exit
	
	# Calculate transaction fees
	entry_fees = entry_ev * transaction_fees_entry
	exit_fees = exit_ev * transaction_fees_exit
	
	# Calculate final equity value after fees
	final_equity = exit_equity - exit_fees
	
	# Calculate return metrics
	return_multiple = final_equity / entry_equity
	irr = (return_multiple ** (1/years) - 1) * 100
	
	# Calculate growth metrics
	revenue_cagr = ((projected_revenue[-1] / starting_revenue) ** (1/years) - 1) * 100
	ebitda_cagr = ((projected_ebitda[-1] / projected_ebitda[0]) ** (1/years) - 1) * 100
	
	# Calculate absolute growth
	revenue_growth = projected_revenue[-1] - starting_revenue
	ebitda_growth = projected_ebitda[-1] - projected_ebitda[0]
	
	# Calculate multiples
	entry_ev_revenue = entry_ev / starting_revenue
	exit_ev_revenue = exit_ev / projected_revenue[-1]
	
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
		st.markdown('### Metric')
		st.markdown('Revenue')
		st.markdown('EBITDA')
		st.markdown('EBITDA Margin')
		st.markdown('EV')
		st.markdown('EV/Revenue')
		st.markdown('EV/EBITDA')
		st.markdown('Net Debt')
		st.markdown('Equity')
		st.markdown('Transaction Fees')
		st.markdown('Return Multiple')
		st.markdown('IRR')
		st.markdown('CAGR')
		st.markdown('Absolute Growth')
	
	with col2:
		st.markdown('### Entry')
		st.metric('', f'${starting_revenue/1_000_000:.1f}M')
		st.metric('', f'${projected_ebitda[0]/1_000_000:.1f}M')
		st.metric('', f'{ebitda_margins[0]*100:.1f}%')
		st.metric('', f'${entry_ev/1_000_000:.1f}M')
		st.metric('', f'{entry_ev_revenue:.1f}x')
		st.metric('', f'{ev_ebitda_multiple:.1f}x')
		st.metric('', f'${net_debt_entry/1_000_000:.1f}M')
		st.metric('', f'${entry_equity/1_000_000:.1f}M')
		st.metric('', f'${entry_fees/1_000_000:.1f}M')
		st.metric('', f'{return_multiple:.1f}x')
		st.metric('', f'{irr:.1f}%')
		st.metric('', f'{revenue_cagr:.1f}%')
		st.metric('', f'${revenue_growth/1_000_000:.1f}M')
	
	with col3:
		st.markdown('### Exit')
		st.metric('', f'${projected_revenue[-1]/1_000_000:.1f}M')
		st.metric('', f'${projected_ebitda[-1]/1_000_000:.1f}M')
		st.metric('', f'{ebitda_margins[-1]*100:.1f}%')
		st.metric('', f'${exit_ev/1_000_000:.1f}M')
		st.metric('', f'{exit_ev_revenue:.1f}x')
		st.metric('', f'{exit_multiple:.1f}x')
		st.metric('', f'${net_debt_exit/1_000_000:.1f}M')
		st.metric('', f'${exit_equity/1_000_000:.1f}M')
		st.metric('', f'${exit_fees/1_000_000:.1f}M')
		st.metric('', f'{return_multiple:.1f}x')
		st.metric('', f'{irr:.1f}%')
		st.metric('', f'{ebitda_cagr:.1f}%')
		st.metric('', f'${ebitda_growth/1_000_000:.1f}M')
	
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
	
	# Add sensitivity analysis
	st.markdown('---')
	st.header('Sensitivity Analysis')
	
	# Create sensitivity matrix
	sensitivity_data = {
		'Revenue Growth': [growth_rate - 0.05, growth_rate, growth_rate + 0.05],
		'EBITDA Margin': [ebitda_margin - 0.02, ebitda_margin, ebitda_margin + 0.02],
		'Exit Multiple': [exit_multiple - 1, exit_multiple, exit_multiple + 1]
	}
	
	sensitivity_df = pd.DataFrame(sensitivity_data)
	
	# Calculate returns for each scenario
	sensitivity_returns = []
	for i in range(len(sensitivity_df)):
		scenario = sensitivity_df.iloc[i]
		scenario_ebitda = starting_revenue * (1 + scenario['Revenue Growth']) ** years * scenario['EBITDA Margin']
		scenario_ev = scenario_ebitda * scenario['Exit Multiple']
		scenario_equity = scenario_ev - net_debt_exit - (scenario_ev * transaction_fees_exit)
		scenario_return = scenario_equity / entry_equity
		sensitivity_returns.append(scenario_return)
	
	sensitivity_df['Return Multiple'] = sensitivity_returns
	sensitivity_df['IRR'] = [(x ** (1/years) - 1) * 100 for x in sensitivity_returns]
	
	# Display sensitivity analysis
	st.dataframe(
		sensitivity_df.style.format({
			'Revenue Growth': '{:.1%}',
			'EBITDA Margin': '{:.1%}',
			'Exit Multiple': '{:.1f}',
			'Return Multiple': '{:.1f}x',
			'IRR': '{:.1f}%'
		}),
		use_container_width=True
	)

except Exception as e:
	st.error(f'An error occurred: {str(e)}')
	st.info('Please check your input values and try again.') 