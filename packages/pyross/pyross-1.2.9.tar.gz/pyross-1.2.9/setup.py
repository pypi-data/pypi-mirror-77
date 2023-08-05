import numpy
import os, sys, re
from setuptools import setup, Extension
from Cython.Build import cythonize
import Cython.Compiler.Options
Cython.Compiler.Options.annotate=True


if 'darwin'==(sys.platform).lower():
    extension = Extension('pyross/*', ['pyross/*.pyx'],
        include_dirs=[numpy.get_include()],
        extra_compile_args=['-mmacosx-version-min=10.9'],
        extra_link_args=['-mmacosx-version-min=10.9'],
    )
else:
    extension = Extension('pyross/*', ['pyross/*.pyx'],
        include_dirs=[numpy.get_include()],
    )


with open("README.md", "r") as fh:
    long_description = fh.read()


cwd = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(cwd, 'pyross', '__init__.py')) as fp:
    for line in fp:
        m = re.search(r'^\s*__version__\s*=\s*([\'"])([^\'"]+)\1\s*$', line)
        if m:
            version = m.group(2)
            break
    else:
        raise RuntimeError('Unable to find own __version__ string')


setup(
    name='pyross',
    version=version,
    url='https://github.com/rajeshrinet/pyross',
    project_urls={
            "Documentation": "https://pyross.readthedocs.io",
            "Source": "https://github.com/rajeshrinet/pyross",
            },
    author='The PyRoss team',
    author_email = 'pyross@googlegroups.com',
    license='MIT',
    description='PyRoss is a numerical library for inference, forecasts,\
                and optimal control of epidemiological models in Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    platforms='tested on Linux, macOS, and windows',
    ext_modules=cythonize([ extension ],
        compiler_directives={'language_level': sys.version_info[0]},
        ),
    libraries=[],
    packages=['pyross'],
    install_requires=['cython','numpy','scipy','matplotlib',
                     'cma','sympy','nlopt','dill','pandas','xlrd'],
    package_data={'pyross': ['*.pxd']},
    include_package_data=True,
    classifiers=[
                'License :: OSI Approved :: MIT License',
                'Programming Language :: Python :: 2',
                'Programming Language :: Python :: 2.7',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.7',
                'Topic :: Scientific/Engineering',
                'Topic :: Scientific/Engineering :: Mathematics',
                'Intended Audience :: Science/Research',
                'Intended Audience :: Education',
                ],
)
