# -*- coding: utf-8 -*-

from setuptools import setup

try:
    import pypandoc
    LDESC = pypandoc.convert_file('README.md', 'rst', format='md')
except (ImportError, IOError, RuntimeError) as e:
    print("Pandoc / pypandoc missing - couldn't create convert README.md to reStructuredText")
    print(str(e))
    LDESC = ''

setup(name='jinja2-render',
      version = '1.2',
      description = 'jinja2-render – A CLI tool to render Jinja2 templates',
      long_description = LDESC,
      author = 'Philipp Klaus',
      author_email = 'philipp.l.klaus@web.de',
      url = 'https://github.com/pklaus/jinja2-render',
      license = 'GPL',
      #packages = ['',],
      py_modules = ['jinja2_render',],
      entry_points = {
          'console_scripts': [
              'jinja2-render = jinja2_render:main',
          ],
      },
      zip_safe = True,
      platforms = 'any',
      install_requires = [
          "jinja2",
      ],
      keywords = 'Context-dependent Jinja2 Template Rendering CLI Docker Dockerfile',
      classifiers = [
          'Development Status :: 4 - Beta',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Topic :: System :: Archiving :: Packaging',
      ]
)
