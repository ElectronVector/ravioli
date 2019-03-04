from setuptools import setup

setup(name='ravioli',
      version='0.1.0',
      description='Checks for spaghetti code',
      long_description='A tool for calculating simple, useful complexity metrics -- notably the Koopman Spaghetti '
                       'Factor (KSF) -- for C. This tool is designed to work especially on embedded software written '
                       'for compilers with non-standard extensions. It works without a compiler or any preprocessing '
                       'required.',
      url='https://github.com/ElectronVector/ravioli',
      author='Matt Chernosky',
      author_email='matt@electronvector.com',
      license='MIT',
      packages=['ravioli'],
      entry_points={
            'console_scripts': ['ravioli=ravioli.ravioli:main'],
      },
      zip_safe=False)
