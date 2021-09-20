from setuptools import setup

setup(
	name='daniel_preconfig',
	version='2.0',
	url='http://github.com/danielbatterystapler/preconfig',
	license='GPLv3',
	packages=['daniel_preconfig'],
	entry_points = {
		'console_scripts': [
			'daniel_preconfig = daniel_preconfig.__main__:main',
		]
	}
)

