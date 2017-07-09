from setuptools import setup, find_packages

setup(
    name="adbons",
    version="0.0.1",
    author="Daniel Bälz",
    author_email="me@dbaelz.de",
    description="""A wrapper for the Android adb tool.
        It's just adb on steroids""",
    keywords="android debug bridge adb",
    license="BSD",
    url="https://github.com/dbaelz/adbons",
    python_requires='>=3.5',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
            "click",
            "pyyaml"
    ],
    entry_points={
         'console_scripts': ['adbons=src.adbons:cli']
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3 :: Only",
        "Intended Audience :: Developers"
    ],
)
