import numpy as np
import pandas as pd

def calculate_projections(
	starting_revenue,
	ebitda_margin,
	ev_ebitda_multiple,
	net_debt_entry,
	working_capital_entry,
	transaction_fees_entry,
	management_rollover,
	years,
	growth_rate,
	margin_improvement,
	exit_multiple,
	net_debt_exit,
	working_capital_exit,
	transaction_fees_exit
):
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
	
	return {
		'df': df,
		'entry_metrics': {
			'revenue': starting_revenue,
			'ebitda': projected_ebitda[0],
			'ebitda_margin': ebitda_margins[0],
			'ev': entry_ev,
			'ev_revenue': entry_ev_revenue,
			'ev_ebitda': ev_ebitda_multiple,
			'net_debt': net_debt_entry,
			'equity': entry_equity,
			'fees': entry_fees
		},
		'exit_metrics': {
			'revenue': projected_revenue[-1],
			'ebitda': projected_ebitda[-1],
			'ebitda_margin': ebitda_margins[-1],
			'ev': exit_ev,
			'ev_revenue': exit_ev_revenue,
			'ev_ebitda': exit_multiple,
			'net_debt': net_debt_exit,
			'equity': exit_equity,
			'fees': exit_fees
		},
		'return_metrics': {
			'multiple': return_multiple,
			'irr': irr,
			'revenue_cagr': revenue_cagr,
			'ebitda_cagr': ebitda_cagr,
			'revenue_growth': revenue_growth,
			'ebitda_growth': ebitda_growth
		}
	}

def calculate_sensitivity(
	starting_revenue,
	ebitda_margin,
	ev_ebitda_multiple,
	net_debt_entry,
	net_debt_exit,
	transaction_fees_exit,
	entry_equity,
	years,
	growth_rate,
	exit_multiple
):
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
	
	return sensitivity_df 