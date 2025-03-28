from setuptools import setup, find_packages

setup(
	name='revenue_projection_app',
	version='0.1.0',
	packages=find_packages(),
	install_requires=[
		'streamlit',
		'pandas',
		'plotly',
		'numpy',
	],
	entry_points={
		'console_scripts': [
			'revenue-calculator=main:main',
		],
	},
) 