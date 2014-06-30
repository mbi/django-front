#!/bin/bash


if [ ! -d .venv_14 ]
then
    virtualenv --no-site-packages --distribute --python=python2.7 .venv_14
    . .venv_14/bin/activate
    pip install Django==1.4 coverage python-memcached django-classy-tags south django-wymeditor six flake8
    deactivate
fi
if [ ! -d .venv_15 ]
then
    virtualenv --no-site-packages --distribute --python=python2.7 .venv_15
    . .venv_15/bin/activate
    pip install Django==1.5 coverage python-memcached django-classy-tags south django-wymeditor six flake8
    deactivate
fi
if [ ! -d .venv_15_p3 ]
then
    virtualenv --no-site-packages --distribute --python=python3 .venv_15_p3
    . .venv_15_p3/bin/activate
    pip install Django==1.5 coverage python3-memcached django-classy-tags south django-wymeditor six flake8
    deactivate
fi
if [ ! -d .venv_16 ]
then
    virtualenv --no-site-packages --distribute --python=python2.7 .venv_16
    . .venv_16/bin/activate
    pip install Django==1.6.1 python-memcached six flake8 django-classy-tags south django-wymeditor
    deactivate
fi
if [ ! -d .venv_16_p3 ]
then
    virtualenv --no-site-packages --distribute --python=python3 .venv_16_p3
    . .venv_16_p3/bin/activate
    pip install Django==1.6.1 python3-memcached six flake8 django-classy-tags south django-wymeditor
    deactivate
fi
if [ ! -d .venv_17c1 ]
then
    virtualenv --no-site-packages --distribute --python=python2.7 .venv_17c1
    . .venv_17c1/bin/activate
    pip install https://www.djangoproject.com/download/1.7c1/tarball/
    pip install python-memcached six flake8 django-classy-tags south django-wymeditor
    deactivate
fi
if [ ! -d .venv_17c1_p3 ]
then
    virtualenv --no-site-packages --distribute --python=python3 .venv_17c1_p3
    . .venv_17c1_p3/bin/activate
    pip install https://www.djangoproject.com/download/1.7c1/tarball/
    pip install python3-memcached six flake8 django-classy-tags south django-wymeditor
    deactivate
fi




. .venv_14/bin/activate
cd test_project
flake8 --ignore=E501 --exclude=migrations --exclude=south_migrations  ../front
python manage.py --version
python manage.py test front
cd ..
deactivate

. .venv_15/bin/activate
cd test_project
python manage.py --version
flake8 --ignore=E501 --exclude=migrations --exclude=south_migrations  ../front
coverage run --rcfile=.coveragerc manage.py test --failfast front
coverage xml
coverage html
cd ..
deactivate

. .venv_15_p3/bin/activate
cd test_project
flake8 --ignore=E501 --exclude=migrations --exclude=south_migrations  ../front
python manage.py --version
python --version
 python manage.py test front
cd ..
deactivate

. .venv_16/bin/activate
cd test_project
flake8 --ignore=E501 --exclude=migrations --exclude=south_migrations  ../front
python manage.py --version
python manage.py test front
cd ..
deactivate

. .venv_16_p3/bin/activate
cd test_project
flake8 --ignore=E501 --exclude=migrations --exclude=south_migrations  ../front
python manage.py --version
python --version
python manage.py test front
cd ..
deactivate

. .venv_17c1/bin/activate
cd test_project
flake8 --ignore=E501 --exclude=migrations --exclude=south_migrations  ../front
python manage.py --version
python manage.py test front
cd ..
deactivate

. .venv_17c1_p3/bin/activate
cd test_project
flake8 --ignore=E501 --exclude=migrations --exclude=south_migrations  ../front
python manage.py --version
python --version
python manage.py test front
cd ..
deactivate
