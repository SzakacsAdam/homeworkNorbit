from setuptools import setup
from setuptools import find_packages

setup(
    name="CoordinateMockApp",
    version="1.0",
    description="Coordinate producet via sockets",
    author="Adam Szakacs",
    author_email="szakacs.adam.98@gmail.com",
    url="https://github.com/SzakacsAdam/homeworkNorbit",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10, <4",
    install_requires=[
        "aiocsv==1.2.3",
        "aiofiles==22.1.0",
        "websockets==10.4"
    ]
)
