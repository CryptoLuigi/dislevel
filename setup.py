from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from setuptools import find_packages, setup

# See note below for more information about classifiers
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Operating System :: MacOS",
    "Operating System :: POSIX :: Linux",
    "Operating System :: Microsoft :: Windows",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
]

current_directory = Path(__file__).parent.resolve()
long_description = (current_directory / "README.md").read_text(encoding="utf-8")

version_path = current_directory / "dendrank" / "_version.py"
module_spec = spec_from_file_location(version_path.name[:-3], version_path)
version_module = module_from_spec(module_spec)
module_spec.loader.exec_module(version_module)

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="dendrank",
    version=version_module.__version__,
    description="A leveling cog for discord bots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CryptoLuigi/dendrank",
    project_urls={
        "Bug Reports": "https://github.com/CryptoLuigi/dendrank/issues",
        "Source": "https://github.com/CryptoLuigi/dendrank",
    },
    author="Michael R",
    author_email="michaelruperto.mr@gmail.com",
    license="MIT",
    classifiers=classifiers,
    keywords="discord discord-rank discord-profile discord-leveling",
    packages=find_packages(),
    python_requires=">=3.7, <4",
    package_data={
        "dendrank": ["assets/*.*"],
    },
    install_requires=requirements,
)
