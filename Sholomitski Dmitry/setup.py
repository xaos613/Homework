from setuptools import setup, find_packages
with open("requirements.txt", encoding="utf-8") as file:
    requirements = file.read()


setup(
    name='rss_reader',
    version='1.2',
    author='Dmitry Sholomitski',
    author_email='xaos613@gmail.com',
    license='BSD_setup.py',
    description='RSS parser',
    py_modules=["rss_reader"],
    long_description='RSS parser using Python v3.10',
    packages=find_packages(),

    install_requires=[requirements],
    python_requires='>=3.10',
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["rss_reader=rss_reader.rss_reader:main"]}
)

