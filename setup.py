from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# 生产环境依赖
requirements = [
    'python-dotenv>=0.19.0',
    'telethon>=1.24.0',
    'pyrogram>=2.0.0',
    'colorlog>=6.6.0',
    'python-dateutil>=2.8.2',
]

setup(
    name="alyce",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A modular Telegram client framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/alyce",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Topic :: Communications :: Chat',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    entry_points={
        'console_scripts': [
            'alyce=alyce.__main__:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/alyce/issues',
        'Source': 'https://github.com/yourusername/alyce',
    },
)
