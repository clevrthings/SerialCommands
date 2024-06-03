from setuptools import setup, find_packages

setup(
    name="ct-serialcommands",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[],
    author="Clevrthings",
    author_email="info@clevrthings.com",
    description="A Python module for seamless serial communication with devices like an Arduino or ESP, offering both non-blocking and blocking interfaces with customizable command and value callbacks.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/clevrthings/SerialCommands",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
