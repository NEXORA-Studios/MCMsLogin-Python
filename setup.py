# -*- coding: utf-8 -*-
"""
Minecraft Microsoft 账户登录模块安装脚本
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mc_ms_login",
    version="0.1.0",
    author="PCL Community",
    author_email="example@example.com",
    description="Minecraft Microsoft 账户登录模块",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/MCMsLogin-Python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment",
    ],
    python_requires=">=3.6",
    install_requires=[
        "msal>=1.20.0",
        "requests>=2.28.0",
    ],
)