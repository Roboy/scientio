import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

required_url = []
required = []
with open("requirements.txt", "r") as freq:
    for line in freq.read().split():
        if "://" in line:
            required_url.append(line)
        else:
            required.append(line)

packages = setuptools.find_packages("src")

setuptools.setup(
    name="scientio",
    version="0.9.1pre",
    url="https://github.com/roboy/scientio",
    author="Roboy",
    author_email="team@roboy.org",

    description="ScientIO is a Knowledge Graph Engine to organise and query complex data.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    package_dir={'': 'src'},
    packages=packages,

    install_requires=required,
    dependency_links=required_url,
    python_requires='>=3.6',

    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
