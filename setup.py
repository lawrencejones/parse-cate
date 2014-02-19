from distutils.core import setup

setup(name='parse-cate',
        version='1.0',
        description="Scraper for Imperial College's CATe system",
        author='Lawrence Jones',
        author_email='lmj112@ic.ac.uk',
        url='http://github.com/lmj112/',
        packages = ['bs4'],
        py_modules=['parse-cate'],
    )
