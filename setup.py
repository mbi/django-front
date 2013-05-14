from setuptools import setup, find_packages
setup(
    name='django-front',
    version='0.1',
    description='A Django application to allow front-end editing',
    author='Marco Bonetti',
    author_email='mbonetti@gmail.com',
    #url='https://github.com/mbi/django-rosetta',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django-classy-tags >= 0.4',
        'django-sekizai >= 0.7',
        'Django >= 1.4'
    ]
)
