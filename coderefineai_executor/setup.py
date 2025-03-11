from setuptools import setup, find_packages

setup(
    name="coderefineai_executor",
    version="0.1.5",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "requests",
        "pydantic",
        "pydantic-settings"
    ],
    author="harish876",
    author_email="harishgokul01@gmail.com",
    url="https://github.com/harish876/CodeRefineAI/coderefineai_executor",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)