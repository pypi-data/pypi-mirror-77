from setuptools import setup

setup(
    name='InterAPI',
    version='0.0.2',
    packages=['InterAPI'],
    url='https://github.com/btmluiz/InterAPI',
    license=open('LICENSE.txt', 'r').read(),
    author='btmluiz',
    author_email='luiz@selectbrasil.com.br',
    description='API para integração com banco inter',
    install_requires=[
        'requests>=2.24.0'
    ],
    python_requires='>=3'
)
