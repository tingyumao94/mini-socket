"""simple set up"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="minisocket", 
    version="0.0.1",
    author="Liuchun Yuan",
    author_email="ylc0003@gmail.com",
    description="socket api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LicharYuan/mini-socket",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)

