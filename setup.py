from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='oktaloginwrapper',
      install_requires=['lxml', 'requests'],
      version='0.2.1',
      description='Okta login made easy from the command line without API token',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/B-Souty/OktaLoginWrapper',
      author='B-Souty',
      author_email='benjamin.souty@gmail.com',
      license='MIT',
      packages=['oktaloginwrapper'],
      classifiers=(
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
      ),)