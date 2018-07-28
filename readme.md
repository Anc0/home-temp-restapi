# Home temp restapi
Api and mqtt subscribing component of the home temp project.

## Setup
There are a few technologies that need to be installed in order for the api to work:

    - postgres      -> $ sudo apt-get install postgresql-10
    - nginx         -> $ sudo apt-get install nginx
    - supervisor    -> $ sudo apt-get install supervisor
    - rabbitmq      -> $ sudo apt-get install rabbitmq-server
    - pip           -> $ sudo apt-get install python-pip


Configure postgres:

    - $ sudo su - postgres
    - $ psql
    - $ CREATE ROLE home_temp WITH PASSWORD 'home_temp';
    - $ ALTER ROLE home_temp with LOGIN;
    - $ CREATE DATABASE home_temp;
    - $ GRANT ALL PRIVILEGES ON DATABASE home_temp to home_temp;


Then install the virtualenv and virtualenvwrapper and create a virtual environment:

    - $ pip install virtualenv virtualenvwrapper
    - $ mkvirtualenv --python=/usr/bin/python3 home-temp-restapi


Lastly create a project directory and deploy the api component of the restapi:

    - $ mkdir ~/home-temp-restapi
    - $ mkdir ~/home-temp-restapi/source
    - on a local machine: $ fab production_api deploy
