from setuptools import setup, find_packages

setup(
    name="celery-pydantic",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "celery>=5.0.0",
        "pydantic>=2.0.0",
        "kombu>=5.0.0",
    ],
    author="Noel Wilson",
    description="A library for serializing Pydantic models in Celery tasks",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/celery_pydantic",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
