# run python -m project

from setuptools import setup, find_packages


setup(
    name='mypackage',
    version='0.0.1',
    install_requires=['requests', 'importlib-metadata; python_version == "3.8"'],

    entry_points={
        'console_scripts': [
            'project = project:startup',
        ]
    },

    # setuptools provides a convenient way to customize which packages should be distributed and in which directory they should be found
    packages= find_packages(where="src"),
    package_dir={"": "src"},
    package_data = {
        "project.data": ["*.txt"],
        "project.data": ["*.png"],

    },
    # The src directory contains all of the source material for building the project
    #package_data={'timmins': ['data/*.png']},  #get all images ending with .png
)
