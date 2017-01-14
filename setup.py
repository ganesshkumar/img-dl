from setuptools import setup

setup(
    name='img-dl',
    version='1.0',
    py_modules=['imgdl'],
    install_requires=[
        'click',
        'validators',
        'beautifulsoup4',
    ],
    entry_points='''
        [console_scripts]
        img-dl=imgdl:imgdl
    '''
)
