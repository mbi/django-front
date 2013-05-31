#!/bin/bash

if [ ! -d .venv_14 ]
then
    virtualenv --no-site-packages --distribute --python=python2 .venv_14
    . .venv_14/bin/activate
    pip install Django==1.4 coverage python-memcached six django-classy-tags south django-wymeditor django-sekizai
    deactivate
fi
if [ ! -d .venv_15 ]
then
    virtualenv --no-site-packages --distribute --python=python2 .venv_15
    . .venv_15/bin/activate
    pip install Django==1.5 coverage python-memcached six django-classy-tags south django-wymeditor django-sekizai
    deactivate
fi


# South doesn't support P3 yet

#if [ ! -d .venv_15_p3 ]
#then
#    virtualenv --no-site-packages --distribute --python=python3 .venv_15_p3
#    . .venv_15_p3/bin/activate
#    pip install Django==1.5 coverage python3-memcached six django-classy-tags south django-wymeditor django-sekizai
#    deactivate
#fi



. .venv_14/bin/activate
cd test_project
python manage.py --version
python manage.py test front
cd ..
deactivate

. .venv_15/bin/activate
cd test_project
python manage.py --version
coverage run --rcfile=.coveragerc manage.py test --failfast front
coverage xml
coverage html
cd ..
deactivate

#. .venv_15_p3/bin/activate
#cd test_project
#python manage.py --version
#python --version
#python manage.py test front
#cd ..
#deactivate

