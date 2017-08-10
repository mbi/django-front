import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as test_command


class Tox(test_command):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        test_command.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        test_command.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)


setup(
    name='django-front',
    version='0.5.6',
    description='A Django application to allow of front-end editing',
    author='Marco Bonetti',
    author_email='mbonetti@gmail.com',
    url='https://github.com/mbi/django-front',
    license='MIT',
    packages=find_packages(exclude=['testproject', 'testproject.*']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django-classy-tags >= 0.4',
        'Django >= 1.7',
        'six'
    ],
    tests_require=['tox'],
    cmdclass={'test': Tox},
)
