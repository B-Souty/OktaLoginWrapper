from setuptools import setup

setup(name='oktaloginwrapper',
      install_requires=['lxml', 'requests'],
      version='0.1',
      description='Okta login made easy from the command line without API token',
      url='https://github.com/B-Souty/OktaLoginWrapper',
      author='B-Souty',
      author_email='benjamin.souty@gmail.com',
      license='MIT',
      packages=['oktaloginwrapper'],
      zip_safe=False)