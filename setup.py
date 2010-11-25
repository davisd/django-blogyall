from distutils.core import setup

setup(
    name='django-blogyall',
    version='0.1.0',
    author='David Davis',
    author_email='davisd@davisd.com',
    packages=['blogyall',],
    url='http://www.davisd.com/projects/django-blogyall',
    license='LICENSE',
    description='django-blogyall is the reusable blog application developed '\
    'for www.davisd.com',
    long_description=open('README').read(),
)