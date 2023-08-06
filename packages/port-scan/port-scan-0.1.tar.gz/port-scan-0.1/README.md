from setuptools import setup, find_packages
setup(
name="Port Scan",
version="0.1",
packages=find_packages(),
scripts=["port-scan.py"],

install_requires=["docutils>=0.3"],

    package_data={
        "": ["*.txt", "*.rst"],
        # And include any *.msg files found in the "hello" package, too:
        "hello": ["*.msg"],
    },

    # metadata to display on PyPI
    author="Gvnn",
    author_email="gionnogodoi@gmail.com",
    description="A port scanner application with python",
    keywords="port scan",
    url=""
    project_urls={
        ""
    },
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License"
    ]

)
