# Flask / Python3 / JWT / Argon2

This project is a simple template to perform signup and login with flask on python3

## Getting Started

git clone THIS REPO

### Prerequisites

What things you need to install the software and how to install them

```
You need to preinstall Python3 on your computer.
Probably is better to use some Docker Image

Also this project uses MySQL 8.0, so use this

$ docker pull mysql:8.0
```

### Installing

Create the VirtualEnv and install dependencies
```
$ python3 -m venv venv
$ . venv/bin/activate
$ pip3 install -r requirements.txt
```

Change settings.py to your MySQL connection DATA

```
mysql+mysqlconnector://root:root@0.0.0.0:3306/database
```

And finally run the project
```
$ python3 server.py
```

this should start the server on
http://0.0.0.0:8080

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Flask](http://flask.pocoo.org/)
* [MySQL 8.0](http://www.mysql.com)

## Authors

* **Cesare Montedonico** - *Initial work* - [Twitter](https://www.twitter.com/cmontedonico)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

