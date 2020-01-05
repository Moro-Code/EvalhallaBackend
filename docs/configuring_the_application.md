---
title: Configuring The Application
permalink: /configuring-the-application/
---

[Home](/) [Site-Map](/site-map)

# Configuring The Application

Make sure you have the prerequisites installed first. Refer to the [prerequisites](/prerequisites) page for more information.

##  Development and Production mode

This application has two seperate modes, development and production. Different configuration variables are required depending on what mode you are running the application in. This goes without saying, but you should ensure you run in production mode when you deploy this application. The docker-compose file will allow you to test both of these modes in a development environment.

To start this application in production simply set the environment variable ```APP_ENV``` to ```production``` and then simply run ```docker-compose up --build``` in your favourite CLI. To run in development set ```APP_ENV``` to ```development``` and then run the docker-compose command specified above. Make sure to include the ```--build``` flag whenever you switch between the two different modes. 





