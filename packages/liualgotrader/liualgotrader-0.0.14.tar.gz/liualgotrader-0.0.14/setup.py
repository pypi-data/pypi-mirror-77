import setuptools

from version import get_git_version

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setuptools.setup(
    name="liualgotrader",
    version=get_git_version(),
    author="amor71",
    author_email="amichay@sgeltd.com",
    description="a Pythonic all-batteries-included framework for effective algorithmic trading. The framework is intended to simplify development, testing, deployment and evaluating algo trading strategies.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amor71/LiuAlgoTrader",
    license="MIT",
    install_requires=requirements,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
