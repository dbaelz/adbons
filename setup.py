from setuptools import setup, find_packages

setup(
    name="adbons",
    version="0.0.1",
    author="Daniel Bälz",
    author_email="me@dbaelz.de",
    description="""A wrapper for the Android adb tool.
        It's just adb on steroids""",
    license="BSD",
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
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
