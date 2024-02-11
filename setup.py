from setuptools import setup

setup(
    name='todomeki',
    version='0.1.1',
    packages=['todomeki'],
    install_requires=[
        'typing-extensions',
        'selenium-screenshot',
        'google-generativeai',
        'setuptools~=66.1.1',
        'selenium~=4.15.2',
        'langchain~=0.0.354',
        'requests~=2.31.0',
    ],
    description='Track event details from web resultse',
    long_description=open('README.md').read(),  # Use the content of your README file
    long_description_content_type='text/markdown',  # Specify the content type
    author='BiscuitBobby',
    url='https://github.com/BiscuitBobby/todomeki',
)
