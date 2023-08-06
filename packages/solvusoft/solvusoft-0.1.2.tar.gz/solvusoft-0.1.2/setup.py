# coding=gbk

from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()


setup(
    name='solvusoft',
    version="0.1.2",
    description=(
        'Solvusoft Library'
    ),
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",
    author='Xie Zheyuan',
    author_email='billy03282@163.com',

    packages=['solvusoftlib'],

    platforms=["all"],
    url='https://github.com/XieZheyuan/solvusoftlib',   # ��������ӣ�һ��дgithub�Ϳ����ˣ����pypi��ת������ȥ
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',

    ],
    install_requires=[
        'requests',
        'beautifulsoup4'
    ]
)