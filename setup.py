from setuptools import setup

setup(name='xmlvirshparser',
      version='0.4',
      description='Parses virsh dump XML output to OpenStack prettytable form',
      long_description=open('README.md').read(),
      url='https://github.com/ervikrant06/virsh_xml_parser',
      author='Vikrant Aggarwal',
      author_email='vaggarwa@redhat.com',
      packages=['xmlvirshparser'],
      install_requires=[
          'xmltodict',
          'prettytable'
      ],
      platforms=['Linux'],
      package_dir={'xmlvirshparser': 'xmlvirshparser'},
      entry_points={
          'console_scripts': [
              'xmlvirshparser=xmlvirshparser:main',
          ],
      },
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5',
          'Topic :: Text Editors :: Text Processing',
          'Topic :: Text Processing :: Markup :: XML',
      ],
)
