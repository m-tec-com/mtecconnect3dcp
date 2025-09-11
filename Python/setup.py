from setuptools import setup, find_packages

setup(
    name="mtecconnect3dcp",
    version="0.0.15",
    author="Paul Richter",
    author_email="paul.richter@m-tec.com",
    description="OPC-UA client classes for m-tec machines (Mixingpump, Printhead, Dosingpump)",
    long_description=open("README.md", encoding="utf-8").read() if __import__('os').path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/m-tec-com/mtecConnect3DCP",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "asyncua>=1.0.0",
        "pyserial>=3.5",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    include_package_data=True,
    keywords="opcua m-tec automation mixingpump pump printhead dosingpump duo-mix flow-matic smp p20 p50",
    project_urls={
        "Source": "https://github.com/m-tec-com/mtecConnect3DCP",
        "Tracker": "https://github.com/m-tec-com/mtecConnect3DCP/issues",
    },
)