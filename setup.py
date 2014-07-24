from distutils.core import setup

setup(
    name='Reddit Live Console',
    version='1.0.0',
    author='Scott Adie',
    author_email='scott@sc0tt.net',
    packages=[],
    scripts=['redditlive.py'],
    url='https://github.com/sc0tt/Reddit-Live-Console',
    license='LICENSE.txt',
    description='Reddit live threads in your console.',
    long_description=open('README.txt').read(),
    install_requires=[
        "requests >= 2.3.0"
    ],
)