from os.path import dirname, join

from setuptools import find_packages, setup

setup(
    name='fefu_admission',
    version='1.9',
    packages=find_packages(),
    long_description_content_type="text/markdown",
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    entry_points={
        'console_scripts':
            ['fefu_admission = fefu_admission.cli:cli']
    },
    install_requires=[
        "certifi==2020.6.20",
        "chardet==3.0.4",
        "click==7.1.2",
        "colorama==0.4.3",
        "idna==2.10",
        "lxml==4.5.2",
        "requests==2.24.0",
        "tabulate==0.8.7",
        "urllib3==1.25.10",
    ],
)
