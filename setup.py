import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="strange-bigmauri",
    version="0.0.1",
    author="Maurizio Bussi",
    author_email="maurizio.bussi.mb@gmail.com",
    description="Python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    project_urls={
        "": "",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.12",
)