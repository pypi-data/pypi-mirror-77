from setuptools import setup, find_packages

d_version = {}
with open("./vipy/version.py") as fp:
    exec(fp.read(), d_version)
version = d_version['VERSION']

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='vipy',
    author='Visym Labs',
    author_email='info@visym.com',
    version=version,
    packages=find_packages(),
    description='Visym Python Tools for Visual Dataset Transformation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/visym/vipy',
    download_url='https://github.com/visym/vipy/archive/%s.tar.gz' % version,
    install_requires=[
        "numpy",
        "matplotlib",
        "dill",
        "pillow",
        "ffmpeg-python"
    ],
    keywords=['vision', 'learning', 'ML', 'CV'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ]
)
