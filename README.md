# Rollladensteuerung

---

## Deployment

### Apache installation
Install the following packages:
```bash
apt install apache2 libapache2-mod-wsgi-py3 python3-dev python3-pip
```
In addition, install the flask pip package:
```bash
pip3 install flask
```

Before removing the default apache web page you can test if apache is working by navigating to the server address in your browser.
Then disable the default apache2 page:
```bash
a2dissite /etc/apache2/sites-available/000-default.conf
```

Add the apache config file for this app (can be found under deployment_files) to /etc/apache2/sites-available.
Enable the new web page by running:
```bash
a2ensite /etc/apache2/sites-available/Rollladensteuerung.conf
```

### Copy files to /var/www/
Copy the flask application files into /var/www/ and change the ownership to www-data:
```bash
git clone https://github.com/Jogi123/Rollladensteuerung.git
chown -R www-data:root Rollladensteuerung
```

### Create wsgi file
Add the wsgi config file (can be found under deployment_files) to /var/www/Rollladensteuerung/

### Folder Structure
Finally, the folder structure relative to /var/www/ should look as follows:
```
`-- Rollladensteuerung
    |-- Rollladensteuerung
    |   |-- __init__.py
    |   |-- routes.py
    |   |-- settings.json
    |   |-- shutters.json
    |   |-- static
    |   |   |-- base.css
    |   |   `-- dashboard.css
    |   `-- templates
    |       |-- dashboard.html
    |       |-- kamera.html
    |       |-- rollladen-add.html
    |       |-- rollladen-delete.html
    |       |-- rollladen-edit.html
    |       |-- rollladen.html
    |       |-- server.html
    |       `-- settings.html
    |-- run.py
    `-- wsgi.py
```

### Relative paths
Make sure to change the files_dir variable in routes.py to "/var/www/data/Rollladensteuerung/" to add absolute paths.
With relative paths, flask will throw a FileNotFoundError. 

### Reload apache to make changes take effect
```bash
systemctl reload apache2
```

---
