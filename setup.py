from setuptools import setup, find_packages

version = '0.4.dev0'

setup(name='affinitic.logging',
      version=version,
      description="Adds information to text logs",
      long_description=open("README.rst").read() + "\n" +
      open("CHANGES.rst").read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.4",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Framework :: Plone",
          "Framework :: Plone :: 3.3",
      ],
      keywords='',
      author='Nicolas Demonte',
      author_email='support@lists.affinitic.be',
      url='https://github.com/affinitic/affinitic.logging',
      license='GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['affinitic'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      extras_require=dict(
          test=['unittest2'],
      ),
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """)
