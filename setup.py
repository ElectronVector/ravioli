from setuptools import setup

setup(name='ravioli',
      version='0.1.0',
      description='Checks for spaghetti code',
      url='https://github.com/ElectronVector/ravioli',
      author='Matt Chernosky',
      author_email='matt@electronvector.com',
      license='MIT',
      packages=['ravioli'],
      entry_points={
            'console_scripts': ['ravioli=ravioli.ravioli:main'],
      },
      zip_safe=False)
