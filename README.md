# Github-projects-tracker

> REST API for tracking organization repositories on Github.

## Table of contents

- [General info](#general-info)
- [Features](#features)
- [Setup](#setup)
- [Authentication](#authentication)
- [API documentation](#api-documentation)
- [Tests](#tests)
- [Technologies](#technologies)
- [Contact](#contact)

## General info

The project aimed to create REST API to monitor organization repositories on Github.
Privileges and the ability to add/view organization repositories depends on Github privacy policy.
Users can be registered by Github token, then they will receive a token to authenticate on app.
The possibility of seeing projects or adding them depends on Github restrictions added by the organization.
The set of monitored projects are the same for all users.

## Features

List of features:
- fully functional REST API
- optimized queries
- register by social provider - Github
- authentication system based on tokens
- automated documentation - swagger/DRF
- selected returned fields like last commit, author, or download link for repo
- protected endpoints
- optimized requests to Github api

## Setup

1 Install Docker and Docker compose

2 Adjust environment variables in [.env](github_projects_tracker/.env)

3 Build image (all commands should be done in project root directory)
```
    docker-compose build
```
4 Run migrations
```
    docker-compose run --rm app ./manage.py migrate
```
5 Create a superuser account to get access for admin panel
```
    docker-compose run --rm app ./manage.py createsuperuser
```
6 Run containers
```
    docker-compose up
```
7 Register OAuth application -> https://github.com/settings/applications/new

For development: 
- Application name: AuthGH
- Homepage URL: http://localhost:8000/
- Authorization callback URL: http://localhost:8000/accounts/github/login/callback/


Keep generated: Client Id and Secret key


8 Register social provider in your app - http://localhost:8000/admin/socialaccount/socialapp/add/

For development
- Provider: Github
- Name: AuthGH
- Client Id: Client Id
- Secret key: Secret key
- Sites: create one (Domain name: http://localhost:8000/, Display name: AuthGithub) and add it to chosen sites

## Authentication

To register and get token app use endpoint and pass your Github token(https://github.com/settings/tokens). Also, use this endpoint if your Github token expires or you lost the app token 

`/api/v1/login_github/`

For development there is added SessionAuthentication, remove this from settings if you want to keep only token-based authentication

## API documentation

Documentation for API can found at this endpoints after running container:

- `/api/v1/documentation/` : Swagger documentation
- `/api/v1/` : Django Rest Framework Browsable API

## Tests

Flake8
```
    docker-compose run --rm app flake8
```

Pytest
```
    docker-compose run --rm app pytest -vv
```

Coverage
```
    docker-compose run --rm app pytest -vv --cov
```

## Technologies

- Python 
- Django 
- Django REST framework 
- PostgreSQL
- Docker
- [Python packages](requirements.txt)

## Contact

Created by <b>Marek Chałabis</b> email: chalabismarek@gmail.com
