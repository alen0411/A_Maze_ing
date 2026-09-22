from setuptools import setup, find_packages

setup(
    name="mazegen",
    version="1.0.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    author="agaube, palvare2",
    description="A standalone, reusable maze generation core library",
)
