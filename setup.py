from setuptools import find_packages, setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='testcase-generator',
    version='0.2.0',
    author='Evan Zhang',
    install_requires=['pyyaml'],
    description='A testcase generator for creating testcases for online judges.',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/Ninjaclasher/testcase-generator',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
    ],
)
