from setuptools import setup


setup(
    name='nose-timing',
    version='0.1',
    description='Useful nose timinmg',
    long_description=open('README.rst').read(),
    author='Andy McKay',
    author_email='andym@mozilla.com',
    license='BSD',
    install_requires=['nose'],
    packages=['timing'],
    url='https://github.com/andymckay/nose-timing',
    entry_points={
        'nose.plugins.0.10': [
            'timing = timing:NoseTiming'
        ]
    },
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Framework :: Django'
    ]
)
