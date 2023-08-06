from setuptools import setup

setup(
	name='pycorda',
	version='0.61',
	author='Jamiel Sheikh',
	packages=['pycorda'],
	install_requires=[
		'jaydebeapi',
		'pandas',
		'matplotlib',
		'datetime',
		'requests',
		'pyjks',
		'chart_studio',
		'scikit-learn',
		'jolokia'
	],
	include_package_data=True,
)