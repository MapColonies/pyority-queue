import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mc-pyority-queue",
    author="MC",
    description="Map colonies priority queue management service for records",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MapColonies/pyority-queue.git",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    # version='0.0.1',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
