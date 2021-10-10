import setuptools

from pychoir.__version__ import version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pychoir",
    version=version,
    author="Antti Kajander",
    author_email="antti.kajander@gmail.com",
    description="Test Matchers for humans",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kajaste/pychoir",
    packages=['pychoir'],
    package_data={"pychoir": ["py.typed"]},
    setup_requires=['setuptools-scm'],
    use_scm_version=dict(
        write_to='pychoir/_version.py',
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
