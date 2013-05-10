from setuptools import setup

setup(
    name='bottu-wolframalpha',
    version='0.1',
    py_modules=['bottu_wolframalpha'],
    url='',
    license='BSD',
    author='Jonas Obrist',
    author_email='ojiidotch@gmail.com',
    description='',
    install_requires=[
        'pyOpenSSL',
        'bottu',
        'wolframalpha',
    ],
    entry_points = {
        'bottu.plugins': [
            'wolframalpha = bottu_wolframalpha:register'
        ],
    }
)
