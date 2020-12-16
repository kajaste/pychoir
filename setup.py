import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pychoir",
    version="0.0.3",
    author="Antti Kajander",
    author_email="antti.kajander@gmail.com",
    description="Matcher templates for humans",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kajaste/pychoir",
    packages=setuptools.find_packages(),
    package_data={"pychoir": ["py.typed"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
