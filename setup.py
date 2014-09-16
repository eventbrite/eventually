from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()

version = '0.1'

install_requires = []


setup(name='eventually',
      version=version,
      description="",
      long_description=README + '\n\n' + NEWS,
      classifiers = [
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
      ],
      keywords='',
      author='Asheesh Laroia',
      author_email='asheesh@eventbrite.com',
      url='https://github.com/eventbrite/eventually',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=install_requires,
      entry_points={
          'console_scripts': [
              'eventually=eventually.cmdline:main',
          ],
      },
)
