from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='vaknl-content',
    description='Vakanties.nl pypi package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version='0.0.2',
    url='https://github.com/vakantiesnl/vaknl-PyPi.git',
    author='Wytze Bruinsma',
    author_email='wytze.bruinsma@vakanties.nl',
    keywords=['vaknl', 'pip'],
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=['Pillow', 'vaknl-gcp']
)
