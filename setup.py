from setuptools import find_packages
from setuptools import setup

with open(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md"), encoding="utf-8",
) as f:
    long_description = f.read()

setup(
    name="princeton-covid",
    version="0.0.1",
    author="Daniel Suo",
    author_email="danielsuo@gmail.com",
    description="COVID-19 data for Princeton, NJ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danielsuo/princeton-covid",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["covid", "Princeton", "New Jersey", "NJ", "covid-19"],
    python_requires=">=3.4",
    install_requires=[
        "numpy",
        "jupyter",
        "pandas",
        "matplotlib"
    ],
)
