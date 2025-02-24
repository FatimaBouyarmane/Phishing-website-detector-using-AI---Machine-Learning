from setuptools import setup, find_packages

setup(
    name="phishing-detector",
    version="1.0.0",
    description="A machine learning-based tool to detect phishing websites.",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "flask",
        "pandas",
        "scikit-learn",
        "requests",
        "tldextract",
        "tkinter",
    ],
    entry_points={
        "console_scripts": [
            "phishing-detector-cli=phishing_detector.predict:main",  # CLI entry point
            "phishing-detector-api=phishing_detector.app:main",      # API entry point
            "phishing-detector-gui=phishing_detector.gui:main",      # GUI entry point
        ],
    },
)