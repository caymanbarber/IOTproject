from setuptools import find_packages, setup
from setuptools.command.build_py import build_py

class NPMInstall(build_py):
    def run(self):
        self.run_command('source cd flaskr/static && npm install jquery')
        self.run_command('source cd flaskr/static && npm install chartjs-adapter-date-fns')
        self.run_command('source cd flaskr/static && npm install chartjs-adapter-moment')
        self.run_command('source cd flaskr/static && npm install chartjs-plugin-zoom')
        self.run_command('source cd flaskr/static && npm install chart.js')
        self.run_command('source cd flaskr/static && npm install chart.js')
        build_py.run(self)

setup(
    name='flaskr',
    version='1.0.0',
    cmdclass={
        'npm_install': NPMInstall
    },
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
