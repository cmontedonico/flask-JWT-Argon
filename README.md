# Flask / Python3 / JWT / Argon2 / MySQL 8 / Nginx / uWSGI

This project is a simple template to perform signup and login with flask on python3

## Getting Started

git clone git@github.com:cmontedonico/flask-JWT-Argon.git

### Prerequisites

What things you need to install the software and how to install them

```
You need to preinstall Python3 on your computer.
Probably is better to use some Docker Image

Also this project uses MySQL 8.0, so use this

$ docker pull mysql:8.0
```

## DOCKERFILE quick testing
Create the image called flask-sample
```
$ docker build -t flask-sample:latest .
```

Then run the image
```
$ docker run -d -p 8080:8080 flask-sample
```

Open this URL to get the API response
http://0.0.0.0:8080


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

## Deployment for production

In production i suggest to use NGINX wiht uWSGI as a service.

```
sudo rm /etc/nginx/sites-enabled/default
sudo ln -s /var/www/flask-JWT-Argon/app_nginx.conf /etc/nginx/conf.d
sudo mkdir -p /var/log/uwsgi
sudo chown ubuntu:www-data /var/log/uwsgi
sudo chmod g+w /var/log/uwsgi
```

Restart nginx, and start uWSGI with our config file (delete the log file after to avoid a permissions issue in the next step).
```
sudo /etc/init.d/nginx restart
rm /var/log/uwsgi/demoapp_uwsgi.log
uwsgi --ini /var/www/flask-JWT-Argon/app_uwsgi.ini
```

Now, visiting the IP address should show our Flask app. However, we want uWSGI to run as a background service, using uWSGI Emperor and systemd. We set up new directories and config files to do so.
```
sudo mkdir -p /etc/uwsgi/vassals
sudo ln -s /var/www/flask-JWT-Argon/app_uwsgi.ini /etc/uwsgi/vassals
sudo cp uwsgi.service /etc/systemd/system
sudo systemctl enable uwsgi
sudo systemctl start uwsgi
```

## Built With

* [Flask](http://flask.pocoo.org/)
* [MySQL 8.0](http://www.mysql.com)

## Authors

* **Cesare Montedonico** - *Initial work* - [Twitter](https://www.twitter.com/cmontedonico)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

