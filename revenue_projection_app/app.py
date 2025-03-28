import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page config
st.set_page_config(
	page_title='Return Calculator',
	page_icon='💰',
	layout='wide',
	initial_sidebar_state='expanded'
)

# CSS
st.markdown("""
<style>
	/* Main container */
	.main .block-container {
		padding-top: 2rem;
	}

	/* Headers */
	h1, h2, h3 {
		font-size: 1.5rem;
		margin-bottom: 1rem;
	}

	/* Dividers */
	hr {
		margin: 0.25rem 0;
	}

	/* Charts */
	.element-container {
		margin-bottom: 1rem;
	}

	/* Dataframes */
	.dataframe {
		font-size: 0.875rem;
	}

	/* Sidebar */
	.css-1d391kg {
		background-color: #f8f9fa;
	}

	/* Number inputs */
	.stNumberInput input {
		font-size: 0.875rem;
	}

	/* Error and info messages */
	.stAlert {
		font-size: 0.875rem;
	}

	/* Metric values */
	.stMetric {
		background-color: #f8f9fa;
		padding: 0.25rem;
		border-radius: 0.25rem;
		margin-bottom: 0.25rem;
		height: 1.5rem;
		display: flex;
		align-items: center;
	}

	.stMetric:hover {
		background-color: #f0f2f6;
	}

	/* Hide metric labels */
	.stMetric label {
		display: none;
	}

	/* Right align values */
	.right-align {
		text-align: right;
	}
</style>
""", unsafe_allow_html=True)

# Title
st.title('Return Calculator')
st.markdown('---')

try:
	# Sidebar inputs
	with st.sidebar:
		st.header('Inputs')
		
		# Financial inputs
		starting_revenue = st.number_input(
			'Starting Revenue ($M)',
			min_value=0.0,
			value=100.0,
			step=1.0
		)
		
		growth_rate = st.number_input(
			'Revenue Growth Rate (%)',
			min_value=-100.0,
			value=10.0,
			step=1.0
		)
		
		ebitda_margin = st.number_input(
			'EBITDA Margin (%)',
			min_value=0.0,
			max_value=100.0,
			value=20.0,
			step=1.0
		)
		
		ev_ebitda_multiple = st.number_input(
			'Entry EV/EBITDA Multiple',
			min_value=0.0,
			value=10.0,
			step=1.0
		)
		
		net_debt_entry = st.number_input(
			'Net Debt at Entry ($M)',
			min_value=0.0,
			value=50.0,
			step=1.0
		)
		
		net_debt_exit = st.number_input(
			'Net Debt at Exit ($M)',
			min_value=0.0,
			value=50.0,
			step=1.0
		)
		
		transaction_fees_exit = st.number_input(
			'Transaction Fees at Exit (%)',
			min_value=0.0,
			max_value=100.0,
			value=2.0,
			step=0.5
		)
		
		# Investment inputs
		years = st.number_input(
			'Hold Period (Years)',
			min_value=1,
			value=5,
			step=1
		)
		
		exit_multiple = st.number_input(
			'Exit EV/EBITDA Multiple',
			min_value=0.0,
			value=12.0,
			step=1.0
		)

	# Calculate projections
	df = pd.DataFrame({
		'Year': range(years + 1),
		'Revenue': starting_revenue * (1 + growth_rate/100) ** list(range(years + 1)),
		'EBITDA': starting_revenue * (1 + growth_rate/100) ** list(range(years + 1)) * (ebitda_margin/100)
	})

	# Calculate entry metrics
	entry_ebitda = df.loc[0, 'EBITDA']
	entry_ev = entry_ebitda * ev_ebitda_multiple
	entry_equity = entry_ev - net_debt_entry

	# Calculate exit metrics
	exit_ebitda = df.loc[years, 'EBITDA']
	exit_ev = exit_ebitda * exit_multiple
	exit_equity = exit_ev - net_debt_exit
	exit_equity_after_fees = exit_equity * (1 - transaction_fees_exit/100)

	# Calculate return metrics
	total_return = (exit_equity_after_fees - entry_equity) / entry_equity * 100
	irr = ((exit_equity_after_fees / entry_equity) ** (1/years) - 1) * 100

	# Display metrics in three columns
	col1, col2, col3 = st.columns(3)

	with col1:
		st.markdown('### Metric')
		st.markdown('Starting Revenue')
		st.markdown('Projected EBITDA')
		st.markdown('EBITDA Margin')
		st.markdown('Entry EV')
		st.markdown('Net Debt')
		st.markdown('Entry Equity')
		st.markdown('EV/EBITDA')
		st.markdown('Transaction Fees')
		st.markdown('Exit EV')
		st.markdown('Exit Equity')
		st.markdown('Exit Equity (After Fees)')
		st.markdown('Total Return')
		st.markdown('IRR')

	with col2:
		st.markdown('### Entry')
		st.markdown(f'${starting_revenue:.1f}M', class_='right-align')
		st.markdown(f'${entry_ebitda:.1f}M', class_='right-align')
		st.markdown(f'{ebitda_margin:.1f}%', class_='right-align')
		st.markdown(f'${entry_ev:.1f}M', class_='right-align')
		st.markdown(f'${net_debt_entry:.1f}M', class_='right-align')
		st.markdown(f'${entry_equity:.1f}M', class_='right-align')
		st.markdown(f'{ev_ebitda_multiple:.1f}x', class_='right-align')
		st.markdown('N/A')
		st.markdown('N/A')
		st.markdown('N/A')
		st.markdown('N/A')
		st.markdown('N/A')
		st.markdown('N/A')

	with col3:
		st.markdown('### Exit')
		st.markdown(f'${df.loc[years, "Revenue"]:.1f}M', class_='right-align')
		st.markdown(f'${exit_ebitda:.1f}M', class_='right-align')
		st.markdown(f'{ebitda_margin:.1f}%', class_='right-align')
		st.markdown(f'${exit_ev:.1f}M', class_='right-align')
		st.markdown(f'${net_debt_exit:.1f}M', class_='right-align')
		st.markdown(f'${exit_equity:.1f}M', class_='right-align')
		st.markdown(f'{exit_multiple:.1f}x', class_='right-align')
		st.markdown(f'{transaction_fees_exit:.1f}%', class_='right-align')
		st.markdown(f'${exit_ev:.1f}M', class_='right-align')
		st.markdown(f'${exit_equity:.1f}M', class_='right-align')
		st.markdown(f'${exit_equity_after_fees:.1f}M', class_='right-align')
		st.markdown(f'{total_return:.1f}%', class_='right-align')
		st.markdown(f'{irr:.1f}%', class_='right-align')

	# Add dividers
	st.markdown('<hr>', unsafe_allow_html=True)
	st.markdown('<hr>', unsafe_allow_html=True)
	st.markdown('<hr>', unsafe_allow_html=True)

	# Charts
	st.header('Projections')
	
	# Revenue and EBITDA chart
	fig_revenue = px.line(
		df,
		x='Year',
		y=['Revenue', 'EBITDA'],
		title='Revenue and EBITDA Projections',
		labels={'value': 'Amount ($M)', 'Year': 'Year'}
	)
	st.plotly_chart(fig_revenue, use_container_width=True)

	# Return waterfall chart
	waterfall_data = pd.DataFrame({
		'Step': ['Entry Equity', 'Revenue Growth', 'Margin Impact', 'Multiple Expansion', 'Net Debt Change', 'Transaction Fees', 'Exit Equity'],
		'Amount': [
			entry_equity,
			df.loc[years, 'Revenue'] - df.loc[0, 'Revenue'],
			df.loc[years, 'EBITDA'] - df.loc[0, 'EBITDA'],
			exit_ev - entry_ev,
			net_debt_entry - net_debt_exit,
			-exit_equity * transaction_fees_exit/100,
			exit_equity_after_fees
		]
	})

	fig_waterfall = go.Figure(go.Waterfall(
		x=waterfall_data['Step'],
		y=waterfall_data['Amount'],
		measure=['relative'] * len(waterfall_data),
		text=waterfall_data['Amount'].apply(lambda x: f'${x:.1f}M'),
		textposition='outside',
		connector={'line': {'color': 'rgb(63, 63, 63)'}},
		hovertemplate='%{x}<br>Amount: %{y:.1f}M<extra></extra>'
	))

	fig_waterfall.update_layout(
		title='Return Waterfall',
		showlegend=False,
		yaxis_title='Amount ($M)',
		height=400
	)

	st.plotly_chart(fig_waterfall, use_container_width=True)

	# Sensitivity Analysis
	st.header('Sensitivity Analysis')
	
	# Create sensitivity matrix
	revenue_range = np.linspace(starting_revenue * 0.8, starting_revenue * 1.2, 5)
	margin_range = np.linspace(ebitda_margin * 0.8, ebitda_margin * 1.2, 5)
	multiple_range = np.linspace(exit_multiple * 0.8, exit_multiple * 1.2, 5)

	sensitivity_data = []
	for rev in revenue_range:
		for margin in margin_range:
			for mult in multiple_range:
				exit_ebitda = rev * (1 + growth_rate/100) ** years * (margin/100)
				exit_ev = exit_ebitda * mult
				exit_equity = exit_ev - net_debt_exit
				exit_equity_after_fees = exit_equity * (1 - transaction_fees_exit/100)
				irr = ((exit_equity_after_fees / entry_equity) ** (1/years) - 1) * 100
				
				sensitivity_data.append({
					'Revenue': rev,
					'Margin': margin,
					'Multiple': mult,
					'IRR': irr
				})

	sensitivity_df = pd.DataFrame(sensitivity_data)

	# Create heatmap
	fig_heatmap = px.density_heatmap(
		sensitivity_df,
		x='Revenue',
		y='Margin',
		z='IRR',
		title='IRR Sensitivity to Revenue and Margin',
		labels={'Revenue': 'Revenue ($M)', 'Margin': 'EBITDA Margin (%)', 'IRR': 'IRR (%)'}
	)
	st.plotly_chart(fig_heatmap, use_container_width=True)

except Exception as e:
	st.error(f'An error occurred: {str(e)}')
	st.info('Please check your input values and try again.') 