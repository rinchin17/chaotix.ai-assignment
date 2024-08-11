# Chaotix.AI assignment - Text to Image (Parallel execution) - By Rinchin Dorjee

## Redis Setup (Linux) 

Install Redis server

```sh
$ sudo apt install redis-server
$ sudo systemctl start redis.service
```

sudo systemctl restart redis.service

## Django Application Setup

Create a directory and enter inside it:
  
```sh
$ mkdir sample-dir
$ cd sample-dir
```

The first thing to do is to clone the repository:
  
```sh
$ git clone https://github.com/rinchin17/chaotix.ai-assignment.git
```
Enter the project directory:
```sh
$cd chaotix.ai-assignment
```
Checkout to the master branch:

```sh
$git checkout master
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ python -m venv env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment

Create a .env file in the root of the project:
1. Contents of the .env file should be:
```sh
SECRET_KEY=your_django_secret_key
STABILITY_API_KEY=your_api_key
STABILITY_API_HOST=stability_api_host
CELERY_BROKER_URL=redis://localhost:6379
```
2. A file named env-example has been provided for reference

Once done, migrate the changes in database :
```sh
(env)$ python manage.py makemigrations
(env)$ python manage.py migrate
```

Collect the static files:
```sh
(env)$ python manage.py collectstatic
```

Start the Django Server:
```sh
(env)$ python manage.py runserver
```

And navigate to `http://127.0.0.1:8000`.

## Start the Celery worker

In another tab/terminal, activate the virtual environment and enter the project directory and run the celery worker:
```sh
 $ cd sample-dir 
 $ source env/bin/activate
(env)$ celery -A image_generator worker -l INFO
```
