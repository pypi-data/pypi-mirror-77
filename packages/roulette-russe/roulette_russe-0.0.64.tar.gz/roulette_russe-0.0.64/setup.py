import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="roulette_russe",
    version="0.0.64",
    author="Mohamed Amjad LASRI",
    author_email="amjadepot@gmail.com",
    description="Library to write your scrapers hassle free.",
    url="https://github.com/Homestr/roulette_russe",
    keywords=['SCRAPING', 'ROULETTE_RUSSE', 'CRAWLING'],
    packages=setuptools.find_packages(),
    install_requires=[
        'vaex',
        'dnspython',
        'boto3',
        'beautifulsoup4',
        'facebook-scraper==0.2.9',
        'linkedin-api~=2.0.0a'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)