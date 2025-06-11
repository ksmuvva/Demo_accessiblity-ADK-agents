"""
Setup configuration for Agents_KM Accessibility Framework
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="agents-km-accessibility",
    version="1.0.0",
    author="Agents_KM Team",
    author_email="team@agents-km.dev",
    description="Accessibility-focused AI Agent Development Kit with WCAG compliance",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/agents-km/accessibility-adk",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.1.0",
            "mypy>=1.7.0",
            "pre-commit>=3.5.0",
        ],
        "ui": [
            "streamlit>=1.28.0",
            "plotly>=5.17.0",
            "dash>=2.14.0",
        ],
        "voice": [
            "speechrecognition>=3.10.0",
            "pyttsx3>=2.90",
            "pyaudio>=0.2.11",
        ],
    },
    entry_points={
        "console_scripts": [
            "agents-km-accessibility=accessibility.cli:main",
            "wcag-validator=accessibility.utils.wcag_validator:main",
            "accessibility-test=accessibility.testing:main",
        ],
    },
    include_package_data=True,
    package_data={
        "accessibility": [
            "config/*.yaml",
            "config/*.json",
            "templates/*.html",
            "static/*",
        ],
    },
    keywords=[
        "accessibility",
        "wcag",
        "ai-agents",
        "adk",
        "a2a",
        "google",
        "gemini",
        "screen-reader",
        "inclusive-design",
    ],
    project_urls={
        "Bug Reports": "https://github.com/agents-km/accessibility-adk/issues",
        "Source": "https://github.com/agents-km/accessibility-adk",
        "Documentation": "https://agents-km.github.io/accessibility-adk/",
    },
) 