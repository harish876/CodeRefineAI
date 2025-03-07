from setuptools import setup, find_packages

setup(
    name="coderefineai-executor",
    version="0.1.0",
    packages=find_packages(include=["core.executor", "core.executor.*"]),
    install_requires=[
        "pandas",
        "pydantic",
        "pydantic-settings",
        "requests",
    ],
    author="harish876",
    author_email="harishgokul01@gmail.com",
    description="A package for executing code submissions.",
    url="https://github.com/harish876/CodeRefineAI/core",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)