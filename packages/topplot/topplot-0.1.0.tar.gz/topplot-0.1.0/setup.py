import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="topplot",
    version="0.1.0",
    author="Jonathan Sambrook",
    author_email="ebardie@gmail.com",
    description="Munge top logs in to graphs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ebardie/topplot",
    packages=["topplot_"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Environment :: X11 Applications",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Logging",
        "Topic :: System :: Monitoring",
    ],
    python_requires=">=3.7",
    install_requires=["matplotlib", "mplcursors", "pandas", "screeninfo"],
    include_package_data=True,
    scripts=["topplot"],
)
