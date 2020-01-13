---
title: Prerequisites
permalink: /prerequisites/
---

[Home](../index.md) [Site-Map](documentation_index.md)

# Prerequisites

This application uses docker for development and production. As such you will need to install docker and ensure that the docker daemon is running. 

If you are using Windows ( excluding WSL2 users ) or MacOS you will need to install docker desktop. Please note you will need a Machine with x86_64 instruction set if you are using Windows or MacOS.


If you are on Windows I highly recommend installing and using [WSL2](https://docs.microsoft.com/en-us/windows/wsl/wsl2-install) instead, it is much simpler to do so. You will be running docker in a linux environment rather than dealing with Windows issues.  If you insist on running Docker through Docker Desktop, please note you will require Windows Pro, Enterprise or Education (Build 15063 or later at the time of writing this documentation)
[Docker Desktop for Windows](https://docs.docker.com/docker-for-windows/install/)


Mac users will need to install
[Docker Desktop for MacOS](https://docs.docker.com/docker-for-mac/install/)


There are many options to install Docker for linux users. See what options is the best for you 
[Docker for Linux](https://docs.docker.com/install/)

If you are planning to run this application in your dev environment, you will also need docker-compose. docker-compose allows you to orchistrate the building and running of multiple containers on your machine. We use this to manage a postgresql container as well as our application container so you don't have to manage an external database for development.

Windows and MacOS users that have installed Docker Desktop already have this. Linux users may need to install docker-compose seperately depending on how Docker was installed. Refer to the [installation documentation](https://docs.docker.com/compose/install/) if you do not have this installed. 

You can also chose to not use docker entirely, But you will have to learn how to configure Celery, RabbitMQ, PostgreSQL, and the application all on your own or until I find the time to write documentation for it :). It's best to just use Docker.... Trust me.
