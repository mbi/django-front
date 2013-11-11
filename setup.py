from setuptools import setup, find_packages
setup(
    name='django-front',
    version='0.2.4',
    description='A Django application to allow of front-end editing',
    author='Marco Bonetti',
    author_email='mbonetti@gmail.com',
    url='https://github.com/mbi/django-front',
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
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django-classy-tags >= 0.4',
        'Django >= 1.4',
        'six'
    ]
)
