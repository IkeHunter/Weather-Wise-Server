# Weather Wise Server Application

### Technology Stack (with documentation link):
| Use | Tech |
| ----------- | ----------- |
| Virtual Environment | [Docker](https://docs.docker.com/get-started/) |
| Language | [Python](https://docs.python.org/3/tutorial/introduction.html) |
| Backend Framework | [Django](https://docs.djangoproject.com/en/4.1/intro/tutorial01/) |
| SQL Database | [Postgres](https://node-postgres.com/) |


## Helpful Links
http://localhost:8000/admin/logic/page/2/change/
http://localhost:8000/api/docs#/weather/weather_results_create
http://localhost:8000/weather/summary/


## Project Prerequisites

In order to properly set up this project on your computer you will need Docker and the latest version of Python installed on your computer (to run things locally, and to configure VSCode virtual env). Here are some links to install Docker:
> Download Docker: [Docker.com](https://www.docker.com/products/docker-desktop/)<br>
> Docker Tutorial: [FreeCodeCamp.org](https://www.freecodecamp.org/news/a-beginners-guide-to-docker-how-to-create-your-first-docker-application-cc03de9b639f/  )

### Virtual ENV
I recommend the use of Conda with python since it's widely used in areas like ML and other Python applications, but you can use `venv` or any other env. You technically don't need this, but VSCode might get mad if you don't set up a Python intrepreter with the correct packages installed.

> Conda Install: [Conda.io](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)<br>
>Conda tutorial: [Conda.io](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html)

## Project Quick Setup
1. Install project from GitHub using `git clone`, then navigate to that new directory

```sh
git clone https://github.com/IkeHunter/Weather_Wise_Server.git

cd Weather_Wise_Server
```
2. Set up Docker.
```sh
docker build .  # builds docker image

docker-compose up  # runs project on port 8000

```

3. Optional: Run tests to ensure everything is installed correctly

```sh
docker-compose run --rm app sh -c "python manage.py test"
```

## Building API with Auto Documentation
You can access a visual representation of the api at this link:
```
http://localhost:8000/api/docs
```

## Helpful Commands

To run weather package in console:
```sh
docker-compose run --rm app sh -c "python logic/weather/main.py"
```

To run tests
```sh
docker-compose run --rm app sh -c "python manage.py test"
```

To start server

```sh
docker-compose up
```


## WTF is Docker

Docker is kinda like a virtual machine you can install on your computer, except this virutal machine contains all the configurations that are needed to run the project. The goal is to enable consistency with dependencies across all machines that run/develop the project.

More technically speaking, Docker runs virtualization software on your machine called "containers", and these essentially sandbox your project from the rest of your machine. Docker creates containers from what they called "images", which are the rules that define how an OS is built - or in this case how a container is built. The image is defined in the `Dockerfile`, and the containers are defined in the `docker-compose.yml` file, but are called "services" when being created with Docker Compose (which is a sort of subset of Docker that makes it easier to run).

If I got any of that wrong, let me know as I am still learning the more technical side of Docker!

### How to use Docker

The most common command you will use when developing this project is the following:
```sh
docker-compose up
```
This command uses docker-compose to build the services (Docker containers) defined in the `docker-compose.yml` file. In this case, it starts up the db, performs any Django preliminary commands, and starts up the Django server.

The next most common command (or most common if you want to use the TDD method - Test Driven Development) is the `docker-compose run` command, and is structured like this:
```sh
docker-compose run [command] [service] [args...]
```
The most common way I use this when development is this:
```sh
# Run tests
docker-compose run --rm app sh -c "python manage.py test"
```
Let's dissect that.

The first item I pass in is a flag `--rm`, this tells docker-compose to remove the containers after they are finished running - which helps keep everything clean, especially if you only use this to pass temporary commands like running tests.

After that, I pass the name of the service to run, in this case it is `app`.

Following the service specifier is the command `sh -c "python manage.py test"`. This command tells docker-compose to overwrite the original command defined in `docker-compose.yml` and run that command instead. In this case we are passing in `python manage.py test`, which is a Django command.

Additionally, you may also encounter the docker-compose command for removing excess containers:
```sh
docker-compose down
```

## Using Django
Django is the actual framework we are using to build the web server, and runs on Python.

Inside the main directory, you will see all of the docker config files, and a directory called `app/`, this directory is where the server app will live. Inside that directory is the `app/` directory (again), `core/` directory, and `manage.py` file. The app directory defines the Django "project", or the overall settings for the application, and the core directory contains the base Django "app", or the actual place a group of functionality lives. The `manage.py` file is where Django processes commands. As the project progresses, we will probably create additional Django "apps" inside the main app directory.

A Django command looks like this:
```sh
python manage.py [command]
```
Where the command is what you want Django to do with your project, like `test`, `runserver`, `startproject`, `starteapp`, etc. Some of these commands take additional arguments, so if you plan on using them make sure you know what commands they take. In this project, we pass that command into the `sh -c [command]` docker-compose command.

To run the server normally, you would run:
```sh
python manage.py runserver 8000
```
This would start the server on port 8000, though you technically could leave the port argument out.

## Bug Fixes Log

### `package drf_spectacular not found`
This error occured in the console when trying to run the docker container for the first time. This error was resolved when activating a virtual env and running the following:
```sh
pip install drf-spectacular
```
A potential reason for this could be docker was trying to access a package from the local system, but it was not installed in the venv it was started in.

## Resources
- https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#inlinemodeladmin-objects
- https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Admin_site
- https://www.geeksforgeeks.org/django-models/
- https://dev.to/tieje/how-to-create-nested-json-in-django-rest-apis-430c
- https://docs.djangoproject.com/en/4.2/ref/models/fields/#integerfield

