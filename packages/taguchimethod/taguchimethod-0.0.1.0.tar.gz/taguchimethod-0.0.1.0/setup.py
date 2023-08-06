from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='taguchimethod',
    version='0.0.1.0',
    description='Taguchi Method',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Akash Sathe',
    author_email='akashsathe79@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='best_levels',
    packages=find_packages(),
    install_requires=['pandas']
)