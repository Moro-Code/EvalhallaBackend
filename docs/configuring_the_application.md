---
title: Configuring The Application
permalink: /configuring-the-application/
---

[Home](../index.md) [Site-Map](documentation_index.md)

# Configuring The Application ⚙️

Make sure you have the prerequisites installed first. Refer to the [prerequisites](/prerequisites) page for more information.

##  Development and Production mode 🏭

This application has two seperate modes, development and production. Different configuration variables are required depending on what mode you are running the application in. This goes without saying, but you should ensure you run in production mode when you deploy this application. The docker-compose file will allow you to test both of these modes in a development environment.

The application is started in production or development based on the value of an environment variable named ```APP_ENV```. To start this application in production simply set the environment variable ```APP_ENV``` to ```production``` and then run ```docker-compose up --build``` in your favourite CLI. To run in development set ```APP_ENV``` to ```development``` and then run the docker-compose command specified above. Make sure to include the ```--build``` flag whenever you switch between the two different modes.

There are a couple of key differences between production mode and development mode.

<table>
  <tr>
    <th>Component</th>
    <th>Production</th>
    <th>Development</th>
  </tr>
  <tr>
    <td>Configuring the Application</td>
    <td>Defaults are not provided for RabbitMQ and PostgreSQL credentials </td>
    <td>Defaults are provided for RabbitMQ and PostgresSQL credentials </td>
  </tr>
  <tr>
    <td> Running the Application</td>
    <td> Run behind multiple gunicorn workers equivalent to the number of CPU cores detected on the system </td>
    <td> <code>flask run</code> is used to start and run the application. This starts a built in WSGI server intended for development purposes only. 
    </td>
  </tr>
  <tr>
    <td> Exceptions </td>
    <td> Uncaught exceptions are not intercepted and the worker is killed as a result. The killed worker will be restarted by gunicorn </td>
    <td> Debugging is turned on, uncaught exceptions are intercepted and a debugging interface is provided by flask at the url ( localhost:5000 ). You can fine more details on this in the [flask documentation](https://flask.palletsprojects.com/en/1.1.x/quickstart/)</td>
  </tr>
  <tr>
    <td>Logging</td>
    <td> No logging is enabled </td>
    <td> Requests and emitted SQL to the PostgreSQL DB are logged to the command line </td>
  </tr>
</table>





