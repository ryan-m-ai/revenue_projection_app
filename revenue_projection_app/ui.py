import streamlit as st
import plotly.express as px

def load_css():
	with open('revenue_projection_app/styles.css') as f:
		st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def render_sidebar():
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
		
		return {
			'starting_revenue': starting_revenue,
			'ebitda_margin': ebitda_margin,
			'ev_ebitda_multiple': ev_ebitda_multiple,
			'net_debt_entry': net_debt_entry,
			'working_capital_entry': working_capital_entry,
			'transaction_fees_entry': transaction_fees_entry,
			'management_rollover': management_rollover,
			'years': years,
			'growth_rate': growth_rate,
			'margin_improvement': margin_improvement,
			'exit_multiple': exit_multiple,
			'net_debt_exit': net_debt_exit,
			'working_capital_exit': working_capital_exit,
			'transaction_fees_exit': transaction_fees_exit
		}

def render_metrics(entry_metrics, exit_metrics, return_metrics):
	col1, col2, col3 = st.columns(3)
	
	with col1:
		st.markdown('### Metric')
		st.markdown('Revenue')
		st.markdown('EBITDA')
		st.markdown('EBITDA Margin')
		st.markdown('<hr>', unsafe_allow_html=True)
		st.markdown('EV')
		st.markdown('EV/Revenue')
		st.markdown('EV/EBITDA')
		st.markdown('<hr>', unsafe_allow_html=True)
		st.markdown('Net Debt')
		st.markdown('Equity')
		st.markdown('Transaction Fees')
		st.markdown('<hr>', unsafe_allow_html=True)
		st.markdown('Return Multiple')
		st.markdown('IRR')
		st.markdown('CAGR')
		st.markdown('Absolute Growth')
	
	with col2:
		st.markdown('### Entry')
		st.markdown(f'<div class="right-align">${entry_metrics["revenue"]/1_000_000:.1f}M</div>', unsafe_allow_html=True)
		st.markdown(f'<div class="right-align">${entry_metrics["ebitda"]/1_000_000:.1f}M</div>', unsafe_allow_html=True)
		st.markdown(f'<div class="right-align">{entry_metrics["ebitda_margin"]*100:.1f}%</div>', unsafe_allow_html=True)
		st.markdown('<hr>', unsafe_allow_html=True)
		st.markdown(f'<div class="right-align">${entry_metrics["ev"]/1_000_000:.1f}M</div>', unsafe_allow_html=True)
		st.markdown(f'<div class="right-align">{entry_metrics["ev_revenue"]:.1f}x</div>', unsafe_allow_html=True)
		st.markdown(f'<div class="right-align">{entry_metrics["ev_ebitda"]:.1f}x</div>', unsafe_allow_html=True)
		st.markdown('<hr>', unsafe_allow_html=True)
		st.markdown(f'<div class="right-align">${entry_metrics["net_debt"]/1_000_000:.1f}M</div>', unsafe_allow_html=True)
		st.markdown(f'<div class="right-align">${entry_metrics["equity"]/1_000_000:.1f}M</div>', unsafe_allow_html=True)
		st.markdown(f'<div class="right-align">${entry_metrics["fees"]/1_000_000:.1f}M</div>', unsafe_allow_html=True)
		st.markdown('<hr>', unsafe_allow_html=True)
		st.markdown(f'<div class="right-align">{return_metrics["multiple"]:.1f}x</div>', unsafe_allow_html=True)
		st.markdown(f'<div class="right-align">{return_metrics["irr"]:.1f}%</div>', unsafe_allow_html=True)
		st.markdown(f'<div class="right-align">{return_metrics["revenue_cagr"]:.1f}%</div>', unsafe_allow_html=True)
		st.markdown(f'<div class="right-align">${return_metrics["revenue_growth"]/1_000_000:.1f}M</div>', unsafe_allow_html=True)
	
	with col3:
		st.markdown('### Exit')
		st.markdown(f'<div class="right-align">${exit_metrics["revenue"]/1_000_000:.1f}M</div>', unsafe_allow_html=True)
		st.markdown(f'<div class="right-align">${exit_metrics["ebitda"]/1_000_000:.1f}M</div>', unsafe_allow_html=True)
		st.markdown(f'<div class="right-align">{exit_metrics["ebitda_margin"]*100:.1f}%</div>', unsafe_allow_html=True)
		st.markdown('<hr>', unsafe_allow_html=True)
		st.markdown(f'<div class="right-align">${exit_metrics["ev"]/1_000_000:.1f}M</div>', unsafe_allow_html=True)
		st.markdown(f'<div class="right-align">{exit_metrics["ev_revenue"]:.1f}x</div>', unsafe_allow_html=True)
		st.markdown(f'<div class="right-align">{exit_metrics["ev_ebitda"]:.1f}x</div>', unsafe_allow_html=True)
		st.markdown('<hr>', unsafe_allow_html=True)
		st.markdown(f'<div class="right-align">${exit_metrics["net_debt"]/1_000_000:.1f}M</div>', unsafe_allow_html=True)
		st.markdown(f'<div class="right-align">${exit_metrics["equity"]/1_000_000:.1f}M</div>', unsafe_allow_html=True)
		st.markdown(f'<div class="right-align">${exit_metrics["fees"]/1_000_000:.1f}M</div>', unsafe_allow_html=True)
		st.markdown('<hr>', unsafe_allow_html=True)
		st.markdown(f'<div class="right-align">{return_metrics["multiple"]:.1f}x</div>', unsafe_allow_html=True)
		st.markdown(f'<div class="right-align">{return_metrics["irr"]:.1f}%</div>', unsafe_allow_html=True)
		st.markdown(f'<div class="right-align">{return_metrics["ebitda_cagr"]:.1f}%</div>', unsafe_allow_html=True)
		st.markdown(f'<div class="right-align">${return_metrics["ebitda_growth"]/1_000_000:.1f}M</div>', unsafe_allow_html=True)

def render_charts(df):
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

def render_sensitivity(sensitivity_df):
	st.markdown('---')
	st.header('Sensitivity Analysis')
	
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