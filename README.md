# DataBase course MIPT Project

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This project repeats the functionality of a more famous application:https://onetimesecret.com/.

## Technologies
Project is created with:
* Django: 2.2.5
* React: 16.13.1
* PostgreSQL: 11.5 
	
## Setup
Firstly, create database and local_settings.py file:

```
$ cd secret_storage/secret_storage
$ vim local_settings.py
```

In this file specify information about database in such format:
![Algorithm schema](../../local_settings.jpg)

To run django application create venv and run server:

```
$ cd secret_storage/
$ python3 -m venv venv
$ source venv/bin/activate/
$ pip install -r requirements.txt
$ python3 manage.py runserver
```
In another tab run frontend application, pre-installing npm:

```
$ cd frontend/
$ npm i
$ npm start
```