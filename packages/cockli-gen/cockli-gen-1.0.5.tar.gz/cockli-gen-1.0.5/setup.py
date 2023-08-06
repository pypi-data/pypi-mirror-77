import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cockli-gen",
    version="1.0.5",
    author="grrfe",
    author_email="grrfe@420blaze.it",
    description="Generate cock.li email addresses on the CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/grrfe/cockli-gen",
    packages=setuptools.find_packages("cockligen"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
    install_requires=['BeautifulSoup4'],
    entry_points={
        'console_scripts': [
            'cockligen = cockligen.__main__:parse_input',
        ],
    }
)
