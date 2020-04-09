from setuptools import setup

# versioning
import versioneer


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="zoop_wrapper",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Imobanco",
    description="Cliente não oficial Zoop",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/imobanco/ZoopAPIWrapper",
    packages=["zoop_wrapper", "zoop_wrapper.models"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Environment :: Web Environment",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: Portuguese (Brazilian)",
        "Operating System :: OS Independent",
        "Topic :: Documentation :: Sphinx",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
        "Topic :: Utilities",
        "",
        "",
    ],
    python_requires=">=3.6",
    install_requires=["requests>=2.23.0", "python-decouple>=3.3", "pycpfcnpj>=1.5.1",],
    keywords="Zoop API client wrapper",
    project_urls={
        "Documentation": "https://imobanco.github.io/ZoopAPIWrapper/",
        "Source": "https://github.com/imobanco/ZoopAPIWrapper",
        "Tracker": "https://github.com/imobanco/ZoopAPIWrapper/issues",
    },
)
