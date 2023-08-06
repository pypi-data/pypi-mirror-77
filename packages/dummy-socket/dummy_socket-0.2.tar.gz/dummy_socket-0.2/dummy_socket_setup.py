from setuptools import setup, find_packages
long=""
setup(
    name="dummy_socket", # Replace with your own username
    version="0.2",
    author="Allen Sun",
    author_email="allen.haha@hotmail.com",
    description="simple socket programming for programmers who want to make effective programs.",
    long_description=long,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['python-whois>=0.7.3'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
