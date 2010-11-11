from setuptools import setup, find_packages

setup(
    name = 'django-testrecorder',
    packages = find_packages(exclude=['tests']),
    include_package_data = True,
    version = '0.1',
    zip_safe = False,
    description = 'Tool for generating tests for Django projects.',
    url = 'https://github.com/pydevua/django-testrecorder'
)
