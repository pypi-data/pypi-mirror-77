# -*- coding: utf-8 -*-

import os

from setuptools import find_packages
from setuptools import setup


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as fh:
        return fh.read()


setup(
    name='rst2pdf',
    python_requires='>=3.6',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    package_dir={'': '.'},
    package_data={
        'rst2pdf': [
            'styles/*.json',
            'styles/*.style',
            'images/*png',
            'images/*jpg',
            'templates/*tmpl',
        ],
    },
    dependency_links=[],
    use_scm_version=True,
    install_requires=[
        'docutils',
        'importlib_metadata',
        'jinja2',
        'packaging',
        'pygments',
        'reportlab',
        'smartypants',
    ],
    extras_require={
        'tests': ['pyPdf2', 'pymupdf'],
        'sphinx': ['sphinx'],
        'hyphenation': ['wordaxe>=1.0'],
        'svgsupport': ['svglib'],
        'aafiguresupport': ['aafigure>=0.4'],
        'mathsupport': ['matplotlib'],
        'rawhtmlsupport': ['xhtml2pdf'],
    },
    # metadata for upload to PyPI
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
        'Topic :: Utilities',
    ],
    author='rst2pdf maintainers',
    author_email='maintainers@rstpdf.org',
    description='Convert reStructured Text to PDF via ReportLab.',
    long_description=read('README.rst'),
    long_description_content_type='text/x-rst',
    license='MIT',
    keywords='restructured convert rst pdf docutils pygments reportlab',
    url='https://rst2pdf.org',
    project_urls={
        'Bug Reports': 'https://github.com/rst2pdf/rst2pdf/issues',
        'Source': 'https://github.com/rst2pdf/rst2pdf',
    },
    download_url='https://github.com/rst2pdf/rst2pdf/releases',
    entry_points={'console_scripts': ['rst2pdf = rst2pdf.createpdf:main']},
)
