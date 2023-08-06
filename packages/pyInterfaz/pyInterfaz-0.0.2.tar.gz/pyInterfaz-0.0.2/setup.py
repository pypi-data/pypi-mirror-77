import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyInterfaz", # Replace with your own username
    version="0.0.2",
    author="Alejandro Lavagnino",
    author_email="alejandro.lavagnino@gmail.com",
    description="Clases para controlar la interfaz + socket",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/astoctas/pyInterfaz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
  install_requires=[            # I get to this in a second
          'pyMata4'
      ],    
    python_requires='>=3.6',
)