from setuptools import setup

setup(name='ravioli',
      version='0.1.0',
      description='Checks for spaghetti code',
      url='https://github.com/ElectronVector/ravioli',
      author='Matt Chernosky',
      author_email='matt@electronvector.com',
      license='MIT',
      packages=['ravioli'],
      install_requires=[
          'pycparser==2.19',
      ],
      zip_safe=False)
