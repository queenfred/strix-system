from setuptools import setup, find_packages
import os


def parse_requirements():
    """
    Parse the project's requirements.txt to populate install_requires.
    """
    here = os.path.abspath(os.path.dirname(__file__))
    req_path = os.path.join(here, os.pardir, 'requirements.txt')
    with open(req_path, encoding='utf-8') as f:
        lines = [l.strip() for l in f if l.strip() and not l.strip().startswith('#')]
    return lines

setup(
    name="strix_security",
    version="0.1.0",
    description="Security module for Strix System (auth, RBAC)",
    author="Tu Nombre u Organización",
    author_email="tu_email@ejemplo.com",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=parse_requirements(),
    python_requires=">=3.8",
)