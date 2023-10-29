# Chatlog API Service

## Project Overview
This can be used by a chat application to populate its users view or update database.

# What I have done
I used flask to write the chatlog api and the tested it using docker image locally then remotly using github action, finally deployed it in heroku

# Local Development
- During the local development I used flask for my backend, 
- flask-sqlalchemy for data since it can be easily converted as postgress database during deployment
- flask server is generate different endpoints, that return json response for call made.
- used Dockerfile to specify flask app configuration to test my application locally

# CI/CD pipeline set up with GitHub Actions.
- configured docker-config.yml file to test application remotely in github actions
- every time commit is made, github action test the application.
- only when all the checks are passed, application is deployed.

this is my config file
name: ci

on:
  push:
    branches:
      - "main"
      
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      -
        name: Checkout
        uses: actions/checkout@v4
      -
        name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: {{ username }}
          password: {{ secured key}}
      -
        name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      -
        name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          file: ./Dockerfile
          push: true
          tags: hanaparthi/chatlog:latest

# Heroku Environment
 - I connected my github repo directly to heroku for deployment
 - used heroku/python for deployment package as my backend needs python
 - I also update my domain name in heroku so that my api can be access using the my domain url

 heroku base url - https://chatlog-webtech-fa086797d6f9.herokuapp.com/
 my base url - https://chatlog.website

 - either urls works but currently my base url doesn't as it might take some time to propagate in the web.