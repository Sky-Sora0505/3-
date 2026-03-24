from setuptools import setup, find_packages

setup(
    name="myproject",
    version="0.1.0",
    author="Your Name",
    author_email="you@example.com",
    description="A sample Python project",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourname/myproject",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={
        "console_scripts": [
            "todo=myproject.cli:main",
            "myshell=myproject.shell:main",
        ],
    },
    python_requires=">=3.9",
    install_requires=[
        # 依存パッケージをここに追加
        # 例: "requests>=2.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
