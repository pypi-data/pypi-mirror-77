from os.path import abspath, dirname

from setuptools import setup

LONG_DESCRIPTION = open(dirname(abspath(__file__)) + "/README.md", "r").read()


setup(
    name="mypy-boto3-comprehend",
    version="1.14.44.0",
    packages=["mypy_boto3_comprehend"],
    url="https://github.com/vemel/mypy_boto3_builder",
    license="MIT License",
    author="Vlad Emelianov",
    author_email="vlad.emelianov.nz@gmail.com",
    description="Type annotations for boto3.Comprehend 1.14.44 service, generated by mypy-boto3-buider 2.2.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Typing :: Typed",
    ],
    keywords="boto3 comprehend type-annotations boto3-stubs mypy typeshed autocomplete auto-generated",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    package_data={"mypy_boto3_comprehend": ["py.typed"]},
    python_requires=">=3.6",
    project_urls={
        "Documentation": "https://mypy-boto3-builder.readthedocs.io/en/latest/",
        "Source": "https://github.com/vemel/mypy_boto3_builder",
        "Tracker": "https://github.com/vemel/mypy_boto3_builder/issues",
    },
    install_requires=["typing_extensions; python_version < '3.8'",],
    zip_safe=False,
)
