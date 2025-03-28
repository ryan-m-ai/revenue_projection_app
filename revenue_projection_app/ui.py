def render_metrics(entry_metrics, exit_metrics, return_metrics):
	# Define sections and their metrics
	sections = {
		'Financials': [
			('Revenue', entry_metrics['revenue'], exit_metrics['revenue']),
			('EBITDA', entry_metrics['ebitda'], exit_metrics['ebitda']),
			('EBITDA Margin', entry_metrics['ebitda_margin']*100, exit_metrics['ebitda_margin']*100, '%'),
		],
		'Valuation': [
			('EV', entry_metrics['ev'], exit_metrics['ev']),
			('EV/Revenue', entry_metrics['ev_revenue'], exit_metrics['ev_revenue'], 'x'),
			('EV/EBITDA', entry_metrics['ev_ebitda'], exit_metrics['ev_ebitda'], 'x'),
			('Net Debt', entry_metrics['net_debt'], exit_metrics['net_debt']),
			('Equity', entry_metrics['equity'], exit_metrics['equity']),
			('Transaction Fees', entry_metrics['fees'], exit_metrics['fees']),
		],
		'Return': [
			('Return Multiple', return_metrics['multiple'], return_metrics['multiple'], 'x'),
			('IRR', return_metrics['irr'], return_metrics['irr'], '%'),
			('Revenue CAGR', return_metrics['revenue_cagr'], return_metrics['revenue_cagr'], '%'),
			('EBITDA CAGR', return_metrics['ebitda_cagr'], return_metrics['ebitda_cagr'], '%'),
			('Revenue Growth', return_metrics['revenue_growth'], return_metrics['revenue_growth']),
			('EBITDA Growth', return_metrics['ebitda_growth'], return_metrics['ebitda_growth']),
		]
	}
	
	# Render each section
	for section_name, metrics in sections.items():
		st.markdown(f'### {section_name}')
		
		# Create three columns for the table
		col1, col2, col3 = st.columns([2, 1, 1])
		
		with col1:
			st.markdown('Metric')
			for metric_name, _, _ in metrics:
				st.markdown(metric_name)
		
		with col2:
			st.markdown('Entry')
			for metric_name, entry_value, _, *suffix in metrics:
				if len(suffix) > 0:
					st.markdown(f'<div class="right-align">{entry_value:.1f}{suffix[0]}</div>', unsafe_allow_html=True)
				else:
					st.markdown(f'<div class="right-align">${entry_value/1_000_000:.1f}M</div>', unsafe_allow_html=True)
		
		with col3:
			st.markdown('Exit')
			for metric_name, _, exit_value, *suffix in metrics:
				if len(suffix) > 0:
					st.markdown(f'<div class="right-align">{exit_value:.1f}{suffix[0]}</div>', unsafe_allow_html=True)
				else:
					st.markdown(f'<div class="right-align">${exit_value/1_000_000:.1f}M</div>', unsafe_allow_html=True)
		
		st.markdown('---') 