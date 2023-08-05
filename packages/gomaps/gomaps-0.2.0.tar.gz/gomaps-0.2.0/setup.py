import setuptools

with open("README.md", 'r') as f:
    long_description = f.read()

setuptools.setup(
    name = "gomaps",
    version = "0.2.0",
    author = "David J. Morfe",
    author_email = "jakemorfe@gmail.com",
    license = "MIT",
    description = "A Google Maps search API for web scraping place data",
    long_description=long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/jakeee51/gomaps",
    install_requires = ["requests_html", "pyppdf", "GeoLiberator"],
    packages = setuptools.find_packages(),
    py_modules = ["gmapss", "busytimes"],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"]
)
