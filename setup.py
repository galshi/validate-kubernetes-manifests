import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="validate_kubernetes_manifests",
    version="0.1.0",
    author="Gal Shinder",
    author_email="galsh1304@gmail.com",
    description="A tool that wraps `kubectl/oc apply --dry-run` to display output in junit-xml format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/galshi/validate-kubernetes-manifests",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)