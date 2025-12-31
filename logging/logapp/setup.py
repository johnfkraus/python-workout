from setuptools import setup, find_packages

setup(
    name="logapp",
    version="0.1.1",
    description="A singleton logger with daily rotation, color output, and YAML/JSON config.",
    author="John Kraus",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pyyaml",
        "colorlog",
    ],
    python_requires=">=3.11",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
)
