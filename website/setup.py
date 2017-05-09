from setuptools import setup

setup(
    name='app',
    packages=['website'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)