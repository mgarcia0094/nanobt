import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nanobt",
    version="0.1.0",
    author="Miguel Ángel García Gandía",
    author_email="mgarcia0094@gmail.com",
    description="A quickly backtesting library for inversion strategies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mgarcia0094/nanobt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)